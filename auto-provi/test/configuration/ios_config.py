import yaml
import sys
from genie.testbed import load
from jinja2 import Environment, FileSystemLoader

# コマンドライン引数をチェック
if len(sys.argv) != 2:
    print("Usage: python script.py <config_file>")
    sys.exit(1)

# ファイル名をコマンドライン引数から取得
config_file = sys.argv[1]

with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

# Jinja2テンプレートを読み込む
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('./template/ios.j2')

# テンプレートに変数を適用する
config = template.render(config)

testbed = load('../tb.yaml')
device = testbed.devices['RT1']

device.connect()

# show runコマンドを実行
output = device.execute('show run')

print(output)

device.configure(config)
                
output = device.execute('show run')

print(output)