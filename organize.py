import os, sys, time, shutil
import fileops, cropframes
import keyframes


def main():

	if sys.argv[1] == 'labels':

		main_dir = './full-clips/train/'
		annotations_file = '_new_shot_type_testuser.txt'

		dir_list = sorted(os.listdir(main_dir))

		label_data = []
		for dir_name in dir_list:
			if os.path.isdir(main_dir + dir_name):
				if os.path.exists(main_dir + dir_name + '/' + dir_name + annotations_file):

					with open(main_dir + dir_name + '/' + dir_name + annotations_file) as labels_file:
						labels = labels_file.readlines()
					labels = [label.split('\t')[0] for label in labels]
					label_data += labels

		label_data = [label + '\n' for label in label_data]
		print len(label_data)

		with open('./labels_list.txt', 'w') as file:
			file.writelines(label_data)			

	elif sys.argv[1] == 'commercials':

		labels_f = sys.arv[2]						## ../trainset/keyframes/label.txt
		keyframes_f = sys.argv[3]


		label_dir = labels_f.rsplit('/',1)[0] + '/'
		trainset_dir = label_dir.rsplit('/',1)[0] + '/'
		frames_path = label_dir + 'cropped/'
		temp = trainset_dir
		if not os.path.exists(temp):
			os.makedirs(temp) 

		with open(labels_f, 'r') as lf:
			label_data = lf.readlines()
		label_data = [label.split('\n') for label in label_data]
		with open(keyframes_f, 'r') as kf:
			keyframes = kf.readlines()
		keyframes_path = [frames_path + keyframe.split('\n') for keyframe in keyframes]

		for idx, label in enumerate(label_data):
			if label not in ['Commercial','Problem/Unclassified']:
				newlabels.append(label + '\n')
				newframes.append(keyframes[idx])
				shutil.copy(keyframes_path[idx], temp)

		with open(temp + 'train.txt', 'w') as file:
			file.writelines(newframes + ' ' + newlabels)




	else:

		clip_path = sys.argv[1] 								## ../../dir/video.mp4
		rel_clip_path = clip_path.rsplit('/',1)[0] + '/'		## ../../dir/
		clip_name = clip_path.rsplit('/',1)[1]					## video.mp4
		clip = clip_name.rsplit('.',1)[0]						## video
		output_filename = clip 									## video
		clip_dir = rel_clip_path								## ../../dir/

		temp = clip_dir + 'keyframes/'							## ../../dir/keyframes/
		if not os.path.exists(temp):
			os.makedirs(temp)

		keyframe_times = keyframes.keyframes(temp, clip_path)
		keyframes_list = fileops.get_keyframeslist(temp, clip_path)

		image_files = cropframes.cropframes(temp, keyframes_list, clip_path)
		image_files = [image_file.rsplit('/',1)[1] + '\n' for image_file in image_files]

		with open(temp + 'keyframes_list.txt', 'aw') as file:
			file.writelines(image_files)


if __name__ == '__main__':
	main()