import os
import sys
import tarfile
import rarfile
import zipfile
import py7zr
import argparse
"""
version: v0.9.2
date: 2023/07/12
usage: will scan folders/files to find c launguage files
       compress file type: zip/rar/tar/7z
TODO: 1) add more function to check if a file is c file;
      2) add more code to check if a file is zip/rar/tar file;
      3) using multi-thread to run check_single_file;
      4) generate a summay file when finish scan.
"""


def is_c_name(file: str) -> bool:
    """
    check if a file name end with .c
    """
    if file.endswith(".c") or file.endswith(".cpp"):
        return True
    return False


def is_zip(file: str) -> bool:
    if file.endswith(".zip"):
        return True
    return False


def is_rar(file: str) -> bool:
    if file.endswith(".rar"):
        return True
    return False


def is_tar(file: str) -> bool:
    if file.endswith(".tar.gz"):
        return True
    return False


def is_7z(file: str) -> bool:
    if file.endswith(".7z"):
        return True
    return False


def check_zip(file: str) -> bool:
    """
    check if a zip file encryted
    check if a zip file has .c files
    """
    status = False
    try:
        zf = zipfile.ZipFile(file)
    except Exception as err:
        print(f"[WARN] Failed to open zip file: {file}, it is not a real zip file")
        return True
    for zinfo in zf.infolist():
        if is_c_name(zinfo.filename):
            print(f'[WARN] Found c file: {zinfo.filename} in zip file: {file}.')
            status = True
        is_encrypted = zinfo.flag_bits & 0x1
        if is_encrypted:
            print(f'[WARN] zip file: {file} encrypted.')
            return True
    return status


def check_rar(file: str) -> bool:
    """
    check if a rar file encryted
    check if a rar file has .c files
    """
    status = False
    try:
        rf = rarfile.RarFile(file)
    except Exception as err:
        print(f"[WARN] Failed to open rar file: {file}, it is not a real rar file")
        return True
    is_encrypted = rf.needs_password()
    if is_encrypted:
        print(f'[WARN] rar file: {file} encrypted.')
        return True
    for name in rf.namelist():
        if is_c_name(name):
            print(f'[WARN] Found c file: {name} in rar file: {file}.')
            status = True
    return status


def check_gz_tar(file: str) -> bool:
    """
    check if a tar file encryted
    check if a tar file has .c files
    """
    status = False
    try:
        zf = tarfile.open(file)
        for name in zf.getnames():
            if is_c_name(name):
                print(f'[WARN] Found c file: {name} in tar file: {file}.')
                status = True
    except Exception as err:
        print(f'[WARN] tar file: {file} error: {err}, maybe encrypted.')
        return True
    return status


def check_7z(file: str) -> bool:
    """
    check if a 7z file encryted
    check if a 7z file has .c files
    """
    status = False
    try:
        with py7zr.SevenZipFile(file, mode='r', password=None) as archive:
            for name in archive.getnames():
                if is_c_name(name):
                    print(f'[WARN] Found c file: {name} in 7z file: {file}.')
                    status = True
    except py7zr.exceptions.PasswordRequired:
        print(f'[WARN] 7z file: {file} encrypted.')
        return True
    except:
        print(f"[WARN] Failed to open 7z file: {file}, maybe it is not a 7z file")
        return True
    return status


def check_single_file(file_name, file_path=None):
    # print(f'[info] check file: {file_name} in {file_path}')
    if file_name in exclude_files:
        print(f'[info] skip check file: {file_name}.')
        return True
    file_full_name = os.path.join(file_path, file_name)
    if is_c_name(file_full_name):
        print(f'[WARN] Found .c file: {file_full_name}')
        return False
    if is_zip(file_full_name):
        return check_zip(file_full_name)
    if is_rar(file_full_name):
        return check_rar(file_full_name)
    if is_tar(file_full_name):
        return check_gz_tar(file_full_name)
    if is_7z(file_full_name):
        return check_7z(file_full_name)
    return True


def main(paths):
    for path in paths:
        if os.path.isfile(path):
            absp = os.path.abspath(path)
            check_single_file(path, file_path=absp)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    check_single_file(file, file_path=root)
        else:
            print(f"[WARN] file: {path} not exist!")


def getParser():
    parser = argparse.ArgumentParser(
        description="Command line parameters for FAST")
    parser.add_argument('-sl', '--scan_list', nargs='+', required=False, default=[],
                        help="scan content in these path, left empty will scan PWD content.")
    parser.add_argument('-ef', '--exclude_files', nargs='+', required=False, default=[],
                        help="skip check these files.")
    return parser


if __name__ == "__main__":
    PWD = os.getcwd()
    TMP = os.path.join(PWD, "scan_temp")
    if not os.path.exists(TMP):
        try:
            os.makedirs(TMP)
        except Exception as err:
            print(f'[ERROR] failed to create temp folder {TMP}, error: {err}')
            sys.exit(1)
    # parse argvs
    arg_parser = getParser()
    args = arg_parser.parse_args()
    scan_list = args.scan_list
    exclude_files = args.exclude_files
    exclude_files.append("scan_temp")
    if len(scan_list) == 0:
        scan_list.append(PWD)
    print(f'[info] will scan files in {scan_list}')
    print(f'[info] will skip files in {exclude_files}')
    # start scan files
    main(scan_list)

