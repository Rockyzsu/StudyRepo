
import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('ml-1m/users.dat', sep='::', header=None, names=unames)
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('ml-1m/ratings.dat', sep='::', header=None, names=rnames)
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('ml-1m/movies.dat', sep='::', header=None, names=mnames)


def foo1():
    # pandas会根据列名的重叠情况推断出哪些是合并（或连接）键
    data = pd.merge(pd.merge(ratings, users), movies)

    # 按性别计算每部电影的平均得分
    # 产生了另一个DataFrame，其内容为电影平均得分，行标为电影名称，列标为性别。
    mean_rating = data.pivot_table('rating', columns='gender', index='title', aggfunc='mean')

    # 过滤掉评分数据不够250条的电影
    ratings_by_title = data.groupby('title').size()
    active_titles = ratings_by_title.index[ratings_by_title >= 250]
    # 该索引中含有评分大于250条的电影名称，然后我们就可以据此从mean_rating中选取所需行了
    mean_rating = mean_rating.ix[active_titles]
    # 为了了解女性观众最喜欢的电影，我们对F列降序排列
    top_female_ratings = mean_rating.sort_index(by='F', ascending=False)
    print(top_female_ratings)


if __name__ == '__main__':
    foo1()
