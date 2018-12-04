import time
import redis

if __name__ == "__main__":
    try:
        conn = redis.StrictRedis(host='192.168.103.31')
        # token_list = ["dbdf7150cb7e013637977faee46d91de",
        #               "0465e280c892013659dc0a5864630fa3",
        #               "4cc82410cb810136b78c0a5864605084",
        #               # "5db2a500cb830136f5420a5864606291",
        #               "1d7a73d0cb840136ce247f5d9393a243",
        #               "82e12d90cb84013694231d671bd17a58",
        #               "d87ddf80cb84013634c50a586461afcb",
        #               "6be48d00cb850136653c0a586461e3e2",
        #               "da9e0e20cb92013633ca779321de6b42",
        #               "0e5d5e00cb930136974369efe9c52225",
        #               "e07b1630cb93013697780a586460a91c",
        #               "100d66f0cb94013633ca779321de6b42",
        #               "5dad3960cb940136f3ec0a5864606161",
        #               "8f7cd690cb940136c22625ca4df7b865",
        #               "bfc1a2a0cb940136b2dd0a58646065da",
        #               "3941c070cb950136081a0a586460ef74",
        #               "6eada440cb950136c86333dc31be71bb",
        #               "d88df440cb950136c22625ca4df7b865",
        #               "472c2580cb96013681f60a5864605d64",
        #               "9b2e72e0cb960136652b0a5864605265",
        #               "e2153c30cb96013628584d55f58d73a2", ]
        token_list = [
            "6ff2fce0cf5b0136652b0a5864605265",
            "c93bb340d9ba0136b650438c3044cd39",
            "ecd0c430d9ba013681240f225e4c64a6",
            "fd9c3290d9ba0136b20239cb45ac4e7e",
            "124f4b40d9bb01366d590a586460e1b5",
            "23106490d9bb01367ac7213168b5ea5a",
            "33d063b0d9bb013609700674ee11f256",
            "44703510d9bb0136087804bdd33225f1",
            "76432ab0d9bb0136c6450a5864607965",
            "885b2510d9bb0136bbda0a586461b1e6",
            "9c480630d9bb0136ae150a5864605c53",
            "ad6e6570d9bb0136a61a7f89c1ef1272",
            "c4517aa0d9bb0136836b0a58646055f3",
            "e40262a0d9bb01368bc30a5864606178",
            "54229ad0d9c10136a8d80a5864631904",
            "95c9e1c0d9c101367db20a5864608ef4",
            "d601df00d9c1013681240f225e4c64a6",
            "0e436b00d9c2013680840d4d12cab342",
            "369ef880d9c201365ee70a5864606e1f",
            "77d1aea0d9c2013609700674ee11f256",
            "a7a37150d9c2013623f05936bf94fd5f",
            "ca3d9dd0d9c2013684e50a586461a8c5",
            "f35c6d40d9c2013669710a5864605ab2",
            "123d4630d9c3013623f05936bf94fd5f",
        ]  # 2018/12/04下午三点半插入的
        for token in token_list:
            conn.lpush("token", token)
        conn.expire('token', 14 * 24 * 60 * 60)  # 设置键的过期时间
    except Exception as err:
        print(err)
