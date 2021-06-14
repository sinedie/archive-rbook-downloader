import os
import time

from .book import Book
from .elements import Button, TextInput


class InternetArchive:
    def __init__(self, driver, log_in_page="https://archive.org/account/login"):
        self.driver = driver
        self.log_in_page = log_in_page

    def log_in(self, email, password):
        self.driver.get(self.log_in_page)
        TextInput(self.driver, "NAME", "username").write((email))
        TextInput(self.driver, "NAME", "password").write((password))
        Button(self.driver, "NAME", "submit-to-login").click()

    def save_book(self, url, output_folder):
        book = Book(self.driver, url)
        book.borrow()
        # book.show_single_page()
        book.zoom()
        book.get_number_pages()

        output_folder = os.path.join(output_folder, book.title)
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        img_folder = os.path.join(output_folder, "/img")
        if not os.path.exists(img_folder):
            os.mkdir(img_folder)

        downloaded = []
        not_downloaded = []
        i = 0
        while i < int(book.n_pages):

            for book_page in book.get_actual_pages():
                if book_page in downloaded:
                    continue

                found = False
                for _ in range(100):  # Wait maximum 100 seconds
                    try:
                        requests = self.driver.requests
                    except:
                        requests = []

                    for request in requests:
                        if not request.response or book_page != request.url:
                            continue

                        found = True
                        downloaded.append(request.url)
                        name = os.path.join(
                            img_folder,
                            f"{str(i).zfill(len(str(book.n_pages)))}.png",
                        )
                        with open(name, "wb") as f:
                            f.write(request.response.body)
                            print(f"{i}.png downloaded")

                        break

                    if found:
                        break
                    else:
                        time.sleep(1)

                if not found:
                    not_downloaded.append(i)
                    print(f"Couldn't download page {i} on {book_page}")

                i += 1
                # input("wait a moment")

            book.next_page()

        book.return_book()

        if len(not_downloaded):
            with open(os.path.join(output_folder, f"errors.txt", "w")) as f:
                f.writelines(not_downloaded)

        book.compress(output_folder, img_folder)

    def download_books(self, urls, output_folder):
        if type(urls) == str:
            urls = [urls]
        if type(urls) != list:
            raise TypeError("URL must be str or list")

        for url in urls:
            self.save_book(url, output_folder)
