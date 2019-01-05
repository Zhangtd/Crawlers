from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
import time
import os
from bs4 import BeautifulSoup
import urllib.request as urlreq

client = ZhihuClient()


class QCrawler:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def client_login(self):
        try:
            client.login(self.username, self.password)
        except NeedCaptchaException:
            with open('captcha.gif', 'wb') as f:
                f.write(client.get_captcha())
            captcha = input('Please input captcha:')
            client.login(self.username, self.password, captcha)
        self.client = client

    def get_image(self, question_id):
        question = self.client.question(question_id)
        imgurl = []
        answers = question.answers
        print("Found %d answers under this question."%len(list(answers)))
        count = 0
        for answer in answers:
            content = answer.content
            soup = BeautifulSoup(content, "html.parser")
            figure_list = soup.find_all("figure")
            if figure_list:
                try:
                    img_list = [figure.img["data-original"] for figure in figure_list]
                    imgurl.append(img_list)
                    count += len(img_list)
                except:
                    continue
        print("Found %d images in these questions."%count)
        save_path = os.getcwd() + "\\question_%d_images\\"%question_id
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        index = 0
        for i in range(len(imgurl)):
            for j in range(len(imgurl[i])):
                url = imgurl[i][j]
                try:
                    urlreq.urlretrieve(url, save_path + str(i) + '_' + str(j) + url[-4:])
                    index += 1
                    if index % 30 == 0:
                        print("Already got %d images." % index)
                except:
                    count = 0
                    while count < 3:
                        print(index)
                        print("Sleeping...")
                        time.sleep(3)
                        try:
                            urlreq.urlretrieve(url, save_path + str(i) + '_' + str(j) + url[-4:])
                            index += 1
                            break
                        except:
                            count += 1

    def get_content(self, question_id):
        question = self.client.question(question_id)
        answers = question.answers
        print("Found %d answers under this question." % len(list(answers)))
        f = open("content.txt", "ab")
        index = 0
        for answer in answers:
            content = answer.content
            content = str(index) + ": " + content + "\n"
            f.write(content.encode())
            index += 1
            if index%50==0:
                print("Already got %d answers."%index)
            if index >= 50:
                break


if __name__ == "__main__":
    username = "Your name"
    password = "Your password"
    question_id = 22856657    # 妹子皂片...
    crawler = QCrawler(username, password)
    crawler.client_login()
    crawler.get_image(question_id)
    crawler.get_content(question_id)



