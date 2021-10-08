import sys
import cv2
import glob
import argparse

parser = argparse.ArgumentParser(description='動画結合用モジュール')

parser.add_argument('-d', '--dir', help='結合する動画の入っているディレクトリ')  # 必須の引数を追加
parser.add_argument('-o', '--out', help='結合後の動画ファイル', default='./default.avi')
parser.add_argument('-t', '--time', help='出力動画の時間[s]', type=int)  # オプション引数（指定しなくても良い引数）を追加

args = parser.parse_args()


def comb_movie(movie_files, out_path):
    # 形式はmp4
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    # 動画情報の取得
    movie = cv2.VideoCapture(movie_files[0])
    fps = movie.get(cv2.CAP_PROP_FPS)
    height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = movie.get(cv2.CAP_PROP_FRAME_WIDTH)

    # 出力先のファイルを開く
    out = cv2.VideoWriter(out_path, int(fourcc), fps, (int(width), int(height)))

    for movies in movie_files:
        print(movies)
        # 動画ファイルの読み込み，引数はビデオファイルのパス
        cap = cv2.VideoCapture(movies)

        if not movie.isOpened():  # 正常に動画ファイルを読み込めたか確認
            print('file cannot open')

        while True:
            # 1フレームずつ取得する。
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)


if __name__ == '__main__':
    # ディレクトリ内の動画をリストで取り出す
    dir_path = args.dir
    if dir_path is None:
        sys.exit(0)
    files = sorted(glob.glob(dir_path + '/*.*'))

    crop_time = sys.maxsize
    if args.time is not None:
        crop_time = int(args.time)

    comb_movie(files, args.out)
