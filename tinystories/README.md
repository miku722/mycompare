tiny stories使用入口

1.将要评估的故事写入test_res.txt文本，格式如下

<img width="1151" alt="image" src="https://github.com/user-attachments/assets/1538c675-b7fa-448d-b8d3-79ecb12b85c8" />


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
