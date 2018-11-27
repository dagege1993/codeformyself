import time
import redis

if __name__ == "__main__":
    try:
        conn = redis.StrictRedis(host='localhost')
        token_list = ["dbdf7150cb7e013637977faee46d91de",
                      "0465e280c892013659dc0a5864630fa3",
                      "4cc82410cb810136b78c0a5864605084",
                      # "5db2a500cb830136f5420a5864606291",
                      "1d7a73d0cb840136ce247f5d9393a243",
                      "82e12d90cb84013694231d671bd17a58",
                      "d87ddf80cb84013634c50a586461afcb",
                      "6be48d00cb850136653c0a586461e3e2",
                      "da9e0e20cb92013633ca779321de6b42",
                      "0e5d5e00cb930136974369efe9c52225",
                      "e07b1630cb93013697780a586460a91c",
                      "100d66f0cb94013633ca779321de6b42",
                      "5dad3960cb940136f3ec0a5864606161",
                      "8f7cd690cb940136c22625ca4df7b865",
                      "bfc1a2a0cb940136b2dd0a58646065da",
                      "3941c070cb950136081a0a586460ef74",
                      "6eada440cb950136c86333dc31be71bb",
                      "d88df440cb950136c22625ca4df7b865",
                      "472c2580cb96013681f60a5864605d64",
                      "9b2e72e0cb960136652b0a5864605265",
                      "e2153c30cb96013628584d55f58d73a2", ]
        for token in token_list:
            conn.lpush("token1", token)
            conn.expire('token', 7 * 24 * 60 * 60)  # 设置键的过期时间为7day
    except Exception as err:
        print(err)