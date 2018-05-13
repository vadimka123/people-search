from piplapis.search import SearchAPIRequest, SearchAPIError


class SocialSearch(object):
    def __init__(self, name):
        self.request = SearchAPIRequest(raw_name=name, api_key='SOCIAL-PREMIUM-DEMO-vllok8b97jwjpygr3p6mnx1x')

    def search(self):
        try:
            return self.request.send()
        except SearchAPIError as e:
            print(e.http_status_code, e)
            return None
