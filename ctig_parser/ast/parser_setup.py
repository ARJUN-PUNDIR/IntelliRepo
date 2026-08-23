import tree_sitter
import tree_sitter_python
from core.logger import setup_logger

logger = setup_logger("ctig_parser.ast")

class ParserManager:
    """
    Manages the Tree-sitter parsers for different languages.
    Currently initializes Python, but built to scale to JS, TS, Java, etc.
    """
    def __init__(self):
        self.parsers = {}
        self._initialize_parsers()

    def _initialize_parsers(self):
        """
        Loads the language grammars and initializes the parsers.
        """
        try:
            # 1. Get the language grammar
            python_lang = tree_sitter.Language(tree_sitter_python.language())
            
            # 2. Create the parser
            parser = tree_sitter.Parser()
            parser.set_language(python_lang)
            
            # 3. Store it in our registry
            self.parsers['python'] = parser
            logger.info("Successfully initialized Tree-sitter Python parser.")
            
        except Exception as e:
            logger.error(f"Failed to initialize parsers: {e}")
            raise

    def get_parser(self, language: str) -> tree_sitter.Parser:
        """
        Retrieves the parser for a specific language.
        """
        parser = self.parsers.get(language.lower())
        if not parser:
            raise ValueError(f"Language '{language}' is not supported yet.")
        return parser

# Singleton instance to be used across the parser module
parser_manager = ParserManager()
