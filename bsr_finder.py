from  amazon.api import AmazonAPI
import secrets, sys

class product_concise(object):
    def __init__(self, title, sales_rank, offer_url, small_image_url):
        self.title = title
        self.sales_rank = sales_rank
        self.offer_url = offer_url
        self.small_image_url = small_image_url

class item_lookup(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def lookup_item_by_keyword(self):
        """
        Returns all results of items given by amazon's search for the supplied keyword
        :param keyword: the keyword to search by
        :return:
        """
        amazon = AmazonAPI(secrets.AMAZON_ACCESS_KEY, secrets.AMAZON_SECRET_KEY, secrets.AMAZON_ASSOC_TAG)
        products = amazon.search(Keywords=self.keyword, SearchIndex='Apparel', MaxQPS=0.9) # might have to remove Sort='salesrank' sort since it grabs tons of different products
        return products

    def products_to_list(self, products):
        """
        creates/returns a list of concise products with only some of the information
        :param products:
        :return:
        """
        product_list = []

        for i, product in enumerate(products):
            title = product.title
            sales_rank = product.sales_rank
            offer_url = product.offer_url
            small_image_url = product.small_image_url
            small_product = product_concise(title=title, sales_rank=sales_rank, offer_url=offer_url, small_image_url=small_image_url)
            product_list.insert(i, small_product)
        return product_list

    def print_products(self, products):
        for i, product in enumerate(products):
            print("{0}. '{1}' {2} {3} {4}".format(i, product.title, product.sales_rank, product.offer_url, product.small_image_url))

class item_list(object):
    def __init__(self, keywords):
        self.list = []
        self.keywords = keywords

    def search_into_list(self):
        # the whole process of searching based on keywords then creating a usable list of data
        lookup = item_lookup(self.keywords)

        try:
            products = lookup.lookup_item_by_keyword()  # get products from Amazon API
            try:
                self.list = lookup.products_to_list(products)  # list of concise products
            except Exception as f:
                print("Exception occurred while converting products to list: " + str(f))
        except Exception as e:
            print("Exception while search Amazon:" + str(e))

        return self.list

def write_to_html(item_list_concise):
    f = open('index.html', 'w', encoding='utf-8')

    f.write("Image --- BSR --- Title and link --- Number of items returned: " + str(len(item_list_concise)) + "\n")

    for product in item_list_concise:
        if (product.small_image_url and product.sales_rank and product.offer_url and product.title):
            f.write("<div><img src='" + product.small_image_url + "'> " + product.sales_rank + " <a href='" + product.offer_url + "'>" + product.title + "</a></div>\n")

    f.close()

if __name__ == '__main__':
    if (len(sys.argv) == 2):
        keyword = sys.argv[1]
    else:
        print("Usage: python bsr_finder.py 'keyword string'")
        sys.exit(0)

    item_list = item_list(keyword)
    item_list_concise = item_list.search_into_list()


    try:
        item_list_concise.sort(key=lambda product: int(product.sales_rank or "999999"))
    except Exception as e:
        print("Exception occurred while sorting results:" + str(e))


    write_to_html(item_list_concise)
