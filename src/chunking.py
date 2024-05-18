import pymupdf

class Chunk:
    def __init__(self, input_file) -> None:
        self.input_file = input_file
        self.chunk_size = 1000
        self.overlap = 100
        self.chunkslist = []

    def chunk(self) -> list:
        with pymupdf.open(self.input_file) as doc:
            text = ""
            start_page = 0
            chunk_num = 1

            for page in doc:
                text += page.get_text()
                
                if len(text) >= self.chunk_size:
                    end_page = start_page + 1

                    while len(text) > self.chunk_size and end_page < doc.page_count:
                        text = text[self.overlap:]
                        end_page += 1

                    chunk = ""
                    for i in range(start_page, end_page):
                        chunk += text
                        
                    self.chunkslist.append(chunk)
                    start_page = end_page
                    chunk_num += 1

        return self.chunkslist


if __name__ == "__main__":
    input_file = 'input_file/xyz.pdf'
    chunker = Chunk(input_file)
    l = chunker.chunk()
    print(len(l))