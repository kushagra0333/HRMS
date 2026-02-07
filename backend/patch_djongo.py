import os
import djongo
from pathlib import Path

def patch_djongo():
    djongo_path = Path(djongo.__file__).parent
    print(f"Djongo found at: {djongo_path}")

    query_py = djongo_path / 'sql2mongo' / 'query.py'
    converters_py = djongo_path / 'sql2mongo' / 'converters.py'

    # Patch query.py
    if query_py.exists():
        content = query_py.read_text()
        
        # Patch 1: SELECT ORDER/GROUP match
        content = content.replace(
            "elif tok.match(tokens.Keyword, 'ORDER'):",
            "elif tok.match(tokens.Keyword, 'ORDER') or tok.match(tokens.Keyword, 'ORDER BY'):"
        )
        content = content.replace(
            "elif tok.match(tokens.Keyword, 'GROUP'):",
            "elif tok.match(tokens.Keyword, 'GROUP') or tok.match(tokens.Keyword, 'GROUP BY'):"
        )

        # Patch 2: Handle Values token in _fill_values
        if "elif type(tok).__name__ == 'Values':" not in content:
            target = "elif tok.match(tokens.Keyword, 'VALUES'):\n                pass"
            replacement = "elif tok.match(tokens.Keyword, 'VALUES'):\n                pass\n            elif type(tok).__name__ == 'Values':\n                self._fill_values(tok)"
            
            if target in content:
                content = content.replace(target, replacement)
            else:
                 print("Warning: Could not find target for _fill_values patch in query.py")
        
        query_py.write_text(content)
        print("Patched query.py")
    else:
        print("Error: query.py not found")

    # Patch converters.py
    if converters_py.exists():
        content = converters_py.read_text()
        
        # Patch OrderConverter.parse
        target_order = "        if not tok.match(tokens.Keyword, 'BY'):\n            raise SQLDecodeError\n\n        tok = self.statement.next()"
        replacement_order = "        if tok.match(tokens.Keyword, 'BY'):\n            tok = self.statement.next()"
        
        if target_order in content:
            content = content.replace(target_order, replacement_order)
            print("Patched OrderConverter in converters.py")
            
        # Patch GroupbyConverter.parse
        target_group = "        if not tok.match(tokens.Keyword, 'BY'):\n            raise SQLDecodeError\n        tok = self.statement.next()"
        replacement_group = "        if tok.match(tokens.Keyword, 'BY'):\n            tok = self.statement.next()"

        if target_group in content:
            content = content.replace(target_group, replacement_group)
            print("Patched GroupbyConverter in converters.py")
            
        converters_py.write_text(content)
    else:
        print("Error: converters.py not found")

if __name__ == "__main__":
    patch_djongo()
    print("Djongo patched successfully.")
