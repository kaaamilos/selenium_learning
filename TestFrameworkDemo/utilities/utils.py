
class Utils:
    def assert_list_item_text(self, item_list, value):
        for item in item_list:
            print(f'the text is: {item.text}')
            assert item.text == value
