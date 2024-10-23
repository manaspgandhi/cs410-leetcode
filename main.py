import PyPDF2
import json

#THIS CLASS IS TO SCRAPE THE DATA FROM THE PDF AND PUT IT INTO A TXT AND JSON FILE
class ScrapeData:
    def __init__(self, pdf_file, txt_file, json_file):
        #define paths to all files
        self.pdf_file = pdf_file
        self.txt_file = txt_file
        self.json_file = json_file

    #pdf_to_txt
    #turns the PDF of blind_75 data into text data in a txt file so we can then convert to a json file
    #@inputs: pdf_path - the path to the pdf we wanna convert into text
    #@outputs: problems.txt - the text file created with the pdf problems
    def pdf_to_txt(self):
        # Open the PDF file in read-binary mode
        with open(self.pdf_file, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            
            # Open the text file in write mode
            with open(self.txt_file, 'w', encoding='utf-8') as text_file:
                # Iterate through all pages in the PDF
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    
                    # Write the extracted text to the file
                    if text:  # Check if text was extracted
                        text_file.write(f"Page {page_num + 1}:\n")  # Optional: Add page markers
                        text_file.write(text)
                        text_file.write("\n\n")  # Add some spacing between pages


    #parse_problem
    #parses a singular problem and extracts the data to be put into a json file
    #@inputs: content - the content from the given page
    #@outputs: problem - the json formatted data of the problem
    def parse_problem(self, content):
        lines = content.splitlines()
        title = lines[0].strip() if len(lines) > 0 else "Unknown Title"
        
        examples = []
        constraints = []
        explanation = ""
        line_num = 0

        #parse through problems.txt
        while line_num < len(lines):
            line = lines[line_num].strip()

            #see if the problem has an example
            if line.startswith("Example"):
                example_input = None
                example_output = None

                #get input if the input exists
                if line_num + 1 < len(lines) and "Input:" in lines[line_num + 1]:
                    example_input = lines[line_num + 1].strip().split("Input:")[1].strip()

                #get output if the output exists
                if line_num + 2 < len(lines) and "Output:" in lines[line_num + 2]:
                    example_output = lines[line_num + 2].strip().split("Output:")[1].strip()

                examples.append({"input": example_input, "output": example_output})
                line_num += 3 #move to next example

            #look for constrains section
            elif line.startswith("Constraints"):
                constraint_lines = []
                while line_num < len(lines) and not lines[line_num].startswith("Example") and lines[line_num]:
                    constraint_lines.append(lines[line_num].strip())
                    line_num += 1
                constraints = " ".join(constraint_lines).strip()  # Join all constraint lines into one string

            #look for explanation section
            elif line.startswith("Explanation:"):
                explanation = line.split("Explanation:")[1].strip()
                line_num += 1
            
            #if nothing then move to the next line
            else:
                line_num += 1

        #json format
        problem = {
            "title": title,
            "examples": examples,
            "explanation": explanation,
            "constraints": constraints
        }
        
        return problem

    #txt_to_json
    #converts data from text (txt) format to json format and puts it into a json file
    #@inputs: none
    #@outputs: problems.json - a json formatted version of the leetcode questions
    #TODO: low key needs to be cleaned up a bit more but im lazy
    def txt_to_json(self):
        #read txt file
        with open(self.txt_file, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()

        #split txt file by pages
        pages = text.split("Page ")[1:]  # We split by "Page " and skip the first empty split

        problems = []

        #parse through txt file page by page
        for page in pages:
            page_number, content = page.split(":", 1)
            problem = self.parse_problem(content.strip())
            problems.append(problem)

        #write results to problems.json
        with open(self.json_file, 'w') as json_file:
            json.dump(problems, json_file, indent=4)

        print("JSON created")


# THIS CLASS IS FOR RUNNING WHATEVER TEXT INFO SYSTEM MODEL WE CHOOSE
class Model:
    def __init__(self, json_file):
        #define paths to json file
        self.json_file = json_file

def main():
    #define file paths
    pdf_file = "problems.pdf"
    txt_file = "problems.txt"
    json_file = "problems.json"

    #first scrape
    scraper = ScrapeData(pdf_file, txt_file, json_file)
    # scraper.pdf_to_text()
    # scraper.txt_to_json()

    #then run the model
    model = Model(json_file)


if __name__ == "__main__":
    main()