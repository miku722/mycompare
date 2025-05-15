# 🚀 Quick Start

## 1. Clone the Repository

```Bash
git clone https://github.com/miku722/mycompare.git

```

## 2. Prepare Your Input File

Create a text file named`test_res.txt`in the`tinystories`directory. 

**Example (****`test_res.txt`****):**

```Markdown
TEST0,    Number of RND_SEED: 23554411683
stories15M, quantize, rv64gcv
MEM_BLOCK_SIZE: 18
Once upon a time, there was a little girl named Lily. She loved to bake cakes with her mommy. One day, they decided to bake a big cake for Lily's birthday. <0x0A>Lily's mommy got out the mixer to mix all the ingredients together. Lily watched as the mixer moved slowly on the spoon. <0x0A>When the cake was ready, they put it in the oven to bake. Lily couldn't wait to try the cake. She took a big bite and it tasted so good! <0x0A>After eating the cake, Lily and her mommy went for a walk. They saw a stream and decided to go swimming. They had so much fun splashing in the water and splpping back and forth. <0x0A>Lily was so happy that she got to bake a cake for her birthday. She couldn't wait for the next one!
achieved tok/s: 3.459547
stories15M, quantize, rv64gcv_vifmm
MEM_BLOCK_SIZE: 18
Once upon a time, there was a little girl named Lily. She loved to sing and dance, but her favorite thing to do was to watch the birds. One day, she saw a big and beautiful birdcage on the ground. It was unknown to her what was inside. <0x0A>Lily decided to pick up the birdcage and take it home. When she got home, she opened the door and the birdcage was filled with a big pile of paper. Lily got a pencil and started to write. She drew a picture of a bird with a pretty feather. <0x0A>When she finished, Lily showed her mommy the drawing. Her mommy was very proud of her and said, "You are such a talented artist!" Lily smiled and felt very happy. From that day on, Lily always went to the birdcage to write and draw with her new feather.
achieved tok/s: 3.383028

```

## 3. Install Dependencies(待补充)

Ensure you have Python 3 installed. Install the required packages using pip:

```Bash
pip install -r requirements.txt
```

*Note: If**`requirements.txt`**is not present, ensure that the necessary modules (**`pandas`**, etc.) are installed.*

## 4. Run the Evaluation Script

Execute the`main.py`script with desired arguments:



```Bash
cd mycompare
python -m tinystories.main --input_file tinystories/test_res.txt --output_file story_output.csv --offline true 
```

**Available Arguments:**

- `--input_file`:Path to the input file containing stories. Default is`test_res.txt`.
- `--output_file`:Path to the output CSV file. Default is`story_evaluations.csv`.
- `--offline`:Set to`true`to use an offline model;`False`to use the online API. Default is`false`.

    如果要使用offline模式：必须先执行ollama run deepseek-r1，其中deepseek-r1为想运行的模型

*Example using an offline model:*

```Bash
python main.py --input_file test_res.txt --output_file story_evaluations.csv --offline true
```

## 5. Review the Output

After execution, the script will generate:

- **`stories.csv`**:Structured CSV containing the extracted stories.
- **`story_evaluations.csv`**:CSV file with evaluation scores and detailed feedback for each story.

## 6. Additional Notes

- **API Key**:Ensure you have a valid API key if using the online mode. Replace the placeholder in the script with your actual API key.
- **Offline Model**:If using the offline mode, ensure that the required local models are properly set up and accessible.
