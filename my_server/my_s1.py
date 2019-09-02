import socket

# 创建对象：socket
# socket 对象  版本1：tcp对象     版本2：udp对象

# 参数1：告知你的ip类型  ipv4（socket.AF_INET）    ipv6
# 参数2：告知你的版本对象  socket.SOCK_STREAM(tcp)

tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_s.setsockopt(socket.SOL_SOCKET, socket.SoL)
# 绑定ip 和端口
tcp_s.bind(("0.0.0.0", 11111))

# 监听 禁用收发数据功能   最大并发数128
tcp_s.listen(128)

# vlue_tup:(新的服务对象， 客户端信息)
while True:
    new_tcp, client_info = tcp_s.accept()
    # 收消息
    browser_info = new_tcp.recv(4096)
    print(browser_info)
    info_list = browser_info.splitlines()       # 按照行 将内容放在列表中

    # 路径信息
    # 将列表中的第一个元素（b'GET / HTTP/1.1\r）拿出来，转成utf-8字符
    index_info = info_list[0].decode("utf-8")

    start = index_info.index("/")
    end = index_info.rindex(" ")        # rindex 从右侧开始找
    # 切出路径信息
    index = index_info[start+1:end]
    print(index)

    # 发消息
    # 给浏览器发消息固定格式


    response_head = "HTTP / 1.1 200 OK\r\n\r\n"
    try:
        # 发送文件
        file = open(index, "rb")
        data = file.read()
        print(data)
    except:
        data = "error 404 not found".encode("utf-8")

    # 编码发送
    new_tcp.send(response_head.encode("utf-8") + data)

    new_tcp.close()