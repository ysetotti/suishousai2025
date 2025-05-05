import subprocess
import time

# リモコン名とボタンコードを定義
remote_name = "code"
button_code = "light_on"

# 赤外線信号の送信
#try:
#    subprocess.run(['ir-ctl', '-s', remote_name, button_code], check=True)
#    print("赤外線信号を送信しました。")
#except subprocess.CalledProcessError as e:
#    print(f"エラーが発生しました: {e}")

# 赤外線信号を受信
try:
#    result = subprocess.run(['ir-ctl','-d /dev/lirc1', '-r'], capture_output=True, text=True, check=True)
#    result = subprocess.run(['ir-ctl','-d /dev/lirc1', '-r','-1'], capture_output=True, text=True)
#    proc = subprocess.Popen(['ir-ctl','-d /dev/lirc1', '-r','-1'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#    command = 'ir-ctl -d /dev/lirc1 -r -1'
    command = 'ir-ctl -d /dev/lirc1 -r'
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        #子から出力が1行あるまで待ち受ける
        line = proc.stdout.readline().decode('utf8', 'replace')
        if line:
            print(line, end='')
#        if not line and proc.poll() is not None:
#            break
#    while result.poll() is None:
#        print("waiting......")
#        time.sleep(1)
#        print(f"受信した信号: {result.stdout.strip()}")
except subprocess.CalledProcessError as e:
    print(f"エラーが発生しました: {e}")
