我有一个一个数据集，我需要你写一个python脚本帮我完成一些任务

数据集的结构如下：

./train/很多json文件和flac文件
./test/很多json文件和flac文件
./valid/很多json文件和flac文件
  

我的python脚本和这些文件夹属于同一个父目录



文件夹里面包含了一些音频文件它们的格式是：

.flac

它们的命名方式是：

编号，例如1.flac. 2.flac

音频的描述文件的路径是：

和音频文件放在一起的，即放在train test valid三个目录下的，对应着各自的音频文件

每个音频描述文件的内容是：

{"text": ["The sounds of Electric guitar, Musical instrument, Guitar, Music and Plucked string instrument"], "tags": ["Musical instrument", "Music", "Electric guitar", "Plucked string instrument", "Guitar", "Electric"], "original_data": {"title": "elecriff3.wav", "description": "Electric guitar.", "license": "http://creativecommons.org/publicdomain/zero/1.0/", "uploader": "UncleSigmund", "fname": "37199", "mids(class_label_id)": ["/m/02sgy", "/m/04szw", "/m/0342h", "/m/04rlf", "/m/0fx80y"]}}


我需要你帮我写代码，把这些数据集整理.成parquet格式的文件，并且上传至huggingface


.parquet文件包含的字段如下：


{index:, datasetname:, audio: , text: "", raw_text: [...], audio_len: }

其中index是string类型，表示音频文件的 路径 + 唯一序列，但是不包含音频文件本身的名字。

例如如果两个音频文件的路径 为 /dataset/train/audio.wav /dataset/train/dog.wav

那么它们的index 分别为： /dataset/train/1    和     /home/train/2

datasetname 的值为 ：FSD50K

audio是音频文件，需要通过huggingface的datasets库来做处理，注意需要直接把音频文件嵌入parquet文件中，而不是直接通过路径的形式。

text：音频文件的台词，有些有有些没有，可以为空

本次任务的台词为每个音频文件对应的json文件的"text"字段，

raw_text: 用的datasets的sequence的格式，内容为对音频文件的描述，可以为空

本次任务的raw_text为每个音频文件对应的json文件的"original_data"字段，

audio_lenth：音频文件的长度


我需要你写的python代码需要我指定目录

例如：可能需要同时指定 ./train ./test ./valid


（也可能只需要指定一个 ./data即可，这些路径下会包含音频文件

还需要我指定音频文件的格式

指定音频描述文件(text)的路径

指定音频描述文件(raw_text)的路径 ， 这两个路径可能是相同的也可能是不同的）

指定输出的目录


可以每100条音频数据生成1个.parquet文件，parquet文件名可以为train-0-train-100.parquet，与index相关，如果到最后仅有不足100条音频数据，也把它们放在一个parquet里，并且做好命名处理即可

如果我指定的目录是./output,那么从train里拿到的数据就要存在./output/train/下面


