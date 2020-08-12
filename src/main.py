import speedtest
import datetime
import socket

from influxdb import InfluxDBClient, DataFrameClient


def influx(body):
    dbhost = "influxdb"
    dbport = "8086"
    dbname = "speedtest"

    client = InfluxDBClient(host=dbhost, port=dbport)
    if client.switch_database(dbname):
        print(f"Using: {dbname}")
    else:
        print(f"DB inexistent, creating: {dbname}")
        client.create_database(dbname)

    try:
        write_response = client.write_points(body)
        return True
    except Exception as e:
        raise e
        return False

def _get_attribute(attr_path):
    try:
        attr = attr_path
    except AttributeError as e:
        attr = ""

    return attr


def main():
    speed_result = speedtest.test()
    host = socket.gethostname()
    body = [
        {
            "measurement": speed_result['server']['sponsor'],
            "tags": {
                "host": host,
                "server_hostname": speed_result['server']['host'],
                "server_id": speed_result['server']['id'],
                "country": speed_result['server']['country'],
                "city": speed_result['server']['name'],
                "cc": speed_result['server']['cc'],
                "isp": speed_result['client']['isp'],
            },
            "time": speed_result['timestamp'],
            "fields": {
                "download": speed_result['download'],
                "upload": speed_result['upload'],
                "ping": speed_result['ping'],
                "bytes_sent": speed_result['bytes_sent'],
                "bytes_received": speed_result['bytes_received'],
                "latency": speed_result['server']['latency']
            }
        }
    ]
    influx(body)

if __name__ == "__main__":
        main()
