import os
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator

# Specify the CIF file folder
cif_folder = "solid_solution"

# Set up XRD calculator
xrd_calculator = XRDCalculator()

# Process CIF files in the folder
for filename in os.listdir(cif_folder):
    if filename.endswith(".cif"):
        cif_file = os.path.join(cif_folder, filename)
        structure = Structure.from_file(cif_file)

        # Calculate XRD pattern
        xrd_pattern = xrd_calculator.get_pattern(structure)

        # Create the output file name
        output_file = os.path.splitext(filename)[0] + ".xy"

        # Save XRD pattern as XY file
        with open(output_file, 'w') as f:
            for i in range(len(xrd_pattern.x)):
                f.write(f"{xrd_pattern.x[i]}, {xrd_pattern.y[i]}\n")

        print("Saved XRD spectrum as XY file:", output_file)


# 원본 폴더 경로
folder_path = "xy file peak"  # 실제 넘파이 파일 폴더 경로로 변경해주세요.

# 새로운 폴더 경로
new_folder_path = "xy spectrum"  # 실제 새로운 폴더 경로로 변경해주세요.

# x 데이터 범위
x_start = 5.00
x_end = 80.00
x_step = 0.01

# 폴더 내의 넘파이 파일 불러오기
np_files = [file for file in os.listdir(folder_path) if file.endswith(".npy")]

# 결과 저장용 리스트 초기화
result = []

# 폴더 내의 넘파이 파일 불러오기
np_files = [file for file in os.listdir(folder_path) if file.endswith(".npy")]

# 결과 저장용 리스트 초기화
result = []

# 넘파이 파일 불러오기 및 데이터 처리
for file in np_files:
    file_path = os.path.join(folder_path, file)

    # 넘파이 배열 로드
    xy_data = np.load(file_path)

    # x 데이터 초기화
    x_data = np.arange(x_start, x_end + x_step, x_step)

    # x 데이터 유효 숫자 설정
    x_data_formatted = np.around(x_data, decimals=2)

    # y 데이터 대입
    new_y_data = []
    for x in x_data_formatted:
        closest_data = min(xy_data, key=lambda d: abs(d[0] - x))
        if abs(closest_data[0] - x) <= 0.01:
            new_y_data.append(closest_data[1])
        else:
            new_y_data.append(0)

    # 결과 저장
    result.append((file, new_y_data))

    # 새로운 파일명 생성
    new_file_name = os.path.splitext(file)[0] + ".xy"
    new_file_path = os.path.join(new_folder_path, new_file_name)

    # 새로운 xy 파일 저장
    with open(new_file_path, 'w') as f:
        for x, y in zip(x_data_formatted, new_y_data):
            f.write("{:.2f} {:.8f}\n".format(x, y))

# 결과 출력
for file, y_data in result:
    print("File: {}".format(file))
    for x, y in zip(x_data, y_data):
        print("{:.2f}: {:.8f}".format(x, y))
    print()