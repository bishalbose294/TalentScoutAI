import fitz
from semantic_text_splitter import TextSplitter
import configparser

config = configparser.ConfigParser()
config.read("TalentScoutAI/configs/config.cfg")
chunk_config = config["CHUNKING"]


class Chunk:
    def __init__(self, chunksize=int(chunk_config["CHUNK_SIZE"]), overlap=int(chunk_config["CHUNK_OVERLAP"])) -> None:
        self.splitter = TextSplitter(capacity=chunksize, overlap=overlap)

    def chunk(self, inputFileLoc) -> list:
        doc = fitz.open(inputFileLoc)

        text = ""
        for page in doc:
            text += " "+ page.get_text()

        chunks = self.splitter.chunks(text)

        return chunks
    
    def getTextFromPdf(self, inputFileLoc) -> list:
        doc = fitz.open(inputFileLoc)

        text = ""
        for page in doc:
            text += " "+ page.get_text()
            
        return text




if __name__ == "__main__":
    input_file = '../test_data/RESUMES/AnanyaDasResume.pdf'
    chunker = Chunk()
    print(chunker.chunk(input_file))