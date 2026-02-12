import os
import djongo
from pathlib import Path

def patch_djongo():
    """
    This script patches the 'djongo' library to fix compatibility issues with newer Django versions.
    Djongo connects Django to MongoDB, but it hasn't been updated recently, so we need to manually
    modify its internal files to prevent crashes.
    """
    
    # Locate where djongo is installed in the site-packages directory.
    djongo_path = Path(djongo.__file__).parent
    print(f"Djongo found at: {djongo_path}")

    # Define paths to the specific files inside djongo that need patching.
    query_py = djongo_path / 'sql2mongo' / 'query.py'
    converters_py = djongo_path / 'sql2mongo' / 'converters.py'

    # --- Patching query.py ---
    if query_py.exists():
        content = query_py.read_text()
        
        # Patch 1: Fix for ORDER BY and GROUP BY syntax.
        # Djongo's original code strictly looks for 'ORDER', but sometimes Django sends 'ORDER BY'.
        # We modify the condition to accept both.
        content = content.replace(
            "elif tok.match(tokens.Keyword, 'ORDER'):",
            "elif tok.match(tokens.Keyword, 'ORDER') or tok.match(tokens.Keyword, 'ORDER BY'):"
        )
        content = content.replace(
            "elif tok.match(tokens.Keyword, 'GROUP'):",
            "elif tok.match(tokens.Keyword, 'GROUP') or tok.match(tokens.Keyword, 'GROUP BY'):"
        )

        # Patch 2: Handle 'Values' token in _fill_values.
        # Sometimes Django generates a 'Values' token that Djongo ignores, causing errors.
        # We check if the patch is already applied; if not, we insert code to handle it.
        if "elif type(tok).__name__ == 'Values':" not in content:
            target = "elif tok.match(tokens.Keyword, 'VALUES'):\n                pass"
            # This replacement adds a check for the 'Values' token type and calls _fill_values.
            replacement = "elif tok.match(tokens.Keyword, 'VALUES'):\n                pass\n            elif type(tok).__name__ == 'Values':\n                self._fill_values(tok)"
            
            if target in content:
                content = content.replace(target, replacement)
            else:
                 print("Warning: Could not find target for _fill_values patch in query.py")
        
        # Write the modified content back to the file.
        query_py.write_text(content)
        print("Patched query.py")
    else:
        print("Error: query.py not found")

    # --- Patching converters.py ---
    if converters_py.exists():
        content = converters_py.read_text()
        
        # Patch OrderConverter.parse and GroupbyConverter.parse
        # The original code raises an error if the 'BY' keyword is missing.
        # We relax this check to make it optional or handled more gracefully.
        
        target_order = "        if not tok.match(tokens.Keyword, 'BY'):\n            raise SQLDecodeError\n\n        tok = self.statement.next()"
        replacement_order = "        if tok.match(tokens.Keyword, 'BY'):\n            tok = self.statement.next()"
        
        if target_order in content:
            content = content.replace(target_order, replacement_order)
            print("Patched OrderConverter in converters.py")
            
        target_group = "        if not tok.match(tokens.Keyword, 'BY'):\n            raise SQLDecodeError\n        tok = self.statement.next()"
        replacement_group = "        if tok.match(tokens.Keyword, 'BY'):\n            tok = self.statement.next()"

        if target_group in content:
            content = content.replace(target_group, replacement_group)
            print("Patched GroupbyConverter in converters.py")
            
        # Write the modified content back to the file.
        converters_py.write_text(content)
    else:
        print("Error: converters.py not found")

if __name__ == "__main__":
    patch_djongo()
    print("Djongo patched successfully.")
