import bs_util


# You're working on a group project, and you just wrote the main function using the code your teammate wrote (in utils).
# Your teammate's test all pass, but your main function runs slower than you'd expect. What is/are the culprit(s)?
def run():
    data = bs_util.make_http_request("https://twitter.com/ArtificalW")
    # Sorted data is faster to search
    data = bs_util.sort(data)
    map = {}
    for tweet in data:
        # find tweet by friend
        if tweet['user']['name'] in map.keys():
            map.get(tweet['user']['name']).append(bs_util.find(data, tweet['user']["friends"]['name']))
        else:
            map[tweet['user']['name']] = [tweet['user']["friends"]['name']]
    bs_util.push_to_DB(map)
    return map

if __name__ == "__main__":
    run()

