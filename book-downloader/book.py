import time
import os
import zipfile


from .elements import Button, Image, Text


class Book:
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.get(url)

    def get_number_pages(self):
        actual_page = Text(
            self.driver,
            "CLASS_NAME",
            "BRcurrentpage",
        ).text

        self.n_pages = actual_page.split()[-1][:-1]

    def get_actual_pages(self):
        # This returns a list. Note the multiple argument
        srcs = Image(
            self.driver,
            "XPATH",
            f"//img[@class='BRpageimage']",
            multiple=True,
        ).src
        srcs.reverse()
        return srcs

    @property
    def title(self):
        return Text(
            self.driver,
            "XPATH",
            f"//h1[@class='item-title']",
        ).text

    def next_page(self):
        Button(
            self.driver,
            "XPATH",
            f"//button[@class='BRicon book_right book_flip_next']",
        ).click()

    def show_single_page(self):
        Button(
            self.driver,
            "XPATH",
            f"//button[@class='BRicon onepg']",
        ).click()

    def zoom(self):
        def get_container():
            return Text(
                self.driver,
                "CLASS_NAME",
                "BRtwopageview",
            )

        div_container = get_container()

        last_height = 1e6
        last_width = 1e6

        while div_container.width != last_width and div_container.height != last_height:
            last_height = div_container.height
            last_width = div_container.width

            Button(self.driver, "XPATH", "//button[@class='BRicon zoom_in']").click()

            div_container = get_container()

    def borrow(self):
        Button(self.driver, "XPATH", "//button[text()='Borrow for 1 hour']").click()

        time.sleep(5)

    def return_book(self):
        Button(self.driver, "XPATH", "//button[text()='Return now']").click()

        time.sleep(5)

    def compress(self, output_folder, target_folder):
        cbz_file = zipfile.ZipFile(
            f"{os.path.join(output_folder, self.title)}.cbz",
            "w",
            zipfile.ZIP_DEFLATED,
        )

        for f in os.listdir(target_folder):
            cbz_file.write(os.path.join(target_folder, f), f)

        cbz_file.close()
