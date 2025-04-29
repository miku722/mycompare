tiny stories使用入口

1.将要评估的故事写入test_res.txt文本，格式如下

  TEST0,    Number of RND_SEED: 23554411683
  stories15M, quantize, rv64gcv
  MEM_BLOCK_SIZE: 18
  Once upon a time, there was a little girl named Lily. She loved to bake cakes with her mommy. One day, they decided to bake a big cake for Lily's birthday. <0x0A>Lily's mommy got out the mixer to mix all the ingredients together. Lily watched as the mixer moved slowly on the spoon. <0x0A>When the cake was ready, they put it in the oven to bake. Lily couldn't wait to try the cake. She took a big bite and it tasted so good! <0x0A>After eating the cake, Lily and her mommy went for a walk. They saw a stream and decided to go swimming. They had so much fun splashing in the water and splpping back and forth. <0x0A>Lily was so happy that she got to bake a cake for her birthday. She couldn't wait for the next one!
  achieved tok/s: 3.459547
  stories15M, quantize, rv64gcv_vifmm
  MEM_BLOCK_SIZE: 18
  Once upon a time, there was a little girl named Lily. She loved to sing and dance, but her favorite thing to do was to watch the birds. One day, she saw a big and beautiful birdcage on the ground. It was unknown to her what was inside. <0x0A>Lily decided to pick up the birdcage and take it home. When she got home, she opened the door and the birdcage was filled with a big pile of paper. Lily got a pencil and started to write. She drew a picture of a bird with a pretty feather. <0x0A>When she finished, Lily showed her mommy the drawing. Her mommy was very proud of her and said, "You are such a talented artist!" Lily smiled and felt very happy. From that day on, Lily always went to the birdcage to write and draw with her new feather.
  achieved tok/s: 3.383028

2.执行方式
跑 main.py
执行成功且结束时当前文件夹会出现两个新文件：
<img width="365" alt="image" src="https://github.com/user-attachments/assets/3f563410-dfae-4f32-bc7b-5800b5ff1402" />
stories.csv为从上述文本中抽取的故事，并组织成csv格式；
story_evaluation为故事的评估分数；
<img width="1340" alt="image" src="https://github.com/user-attachments/assets/b7571297-4882-4e22-bc97-d06b89edbc2c" />



3.extract_stories.py抽取出了故事
  evaluate.py 调用大模型评估故事
  main.py为主程序
