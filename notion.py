#!/usr/bin/env python3

import requests


class notion_exception(Exception):
    """Base Exception Class for Notion API"""

    def __init__(self, value):
        self.message = value

    def __str__(self):
        return repr(self.message)


class token_not_found_exception(notion_exception):
    """Raised when a Token was not provided"""

    pass


class api:
    """SDK for Notion API V1, Notion-Version: 2021-05-13. Supports internal integration type only.

    Parameters:
        token (str): Internal Integration Token (public integrations not supported)
    """

    def __init__(self, token=None):
        self.session = requests.Session()
        # **************************************************************************
        # Section: HTTP Method, direct access
        # **************************************************************************
        self.delete = self.session.delete
        self.get = self.session.get
        self.patch = self.session.patch
        self.post = self.session.post
        self.put = self.session.put
        # **************************************************************************
        # Section: Session setup
        # **************************************************************************
        self.notion_api = "https://api.notion.com/v1/"
        if not token:
            raise token_not_found_exception("No access token")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "Application/JSON",
            "Notion-Version": "2021-05-13",
        }

    # **************************************************************************
    # Section: Endpoints
    # **************************************************************************

    # **************************************************************************
    # Sub-Section: Search
    # **************************************************************************
    def search(self, query=None, sort=None, filter=None):
        """Searches all pages and child pages that are shared with the integration.
        The results may include databases.
        The `query` parameter matches against the page titles. If the `query` parameter
        is not provided, the response will contain all pages (and child pages) in the results.
        The `filter` parameter can be used to query specifically for only pages or
        only databases.
        The response may contain fewer than `page_size` of results. See
        [Pagination](https://developers.notion.com/reference-link/pagination) for details
        about how to use a cursor to iterate through the list.\n
        🚧 Search indexing is not immediate!,
        If an integration performs a search quickly after a page is shared with the integration
        (such as immediately after a user performs OAuth), the response may not contain the page.
        When an integration needs to present a user interface that depends on search results,
        we recommend including a Refresh button to retry the search. This will allow users to
        determine if the expected result is present or not, and give them a means to try again.\n
        Parameters:
            query (str): When supplied, limits which pages are returned by comparing the
            query to the page title.\n
            sort (obj): When supplied, sorts the results based on the provided criteria.
                direction (str): The direction to sort, ascending | descending
                timestamp (str): last_edited_time\n
            filter (obj): When supplied, filters the results based on the provided criteria.
                value (str): The value of the property to filter the results by.
                    Limitation: Currently the only filter allowed is object which will
                    filter by type of object (either page or database)
                property (str): The name of the property to filter by.
                    Limitation: Currently the only filter allowed is object which will
                    filter by type of object (either page or database)
        """
        data = None
        if query or sort or filter:
            data = {}
            if query:
                data["query"] = query
            if sort:
                data["sort"] = sort
            if filter:
                data["filter"] = filter

        r = self.session.post(
            self.notion_api + "search", headers=self.headers, json=data
        )
        return r

    # **************************************************************************
    # Sub-Section: Databases
    # **************************************************************************
    # NOTE: list_databases endpoint is not included as Notion now recomends using
    # "search" instead

    def retrieve_a_database(self, database_id):
        """Retrieves a [Database object](https://developers.notion.com/reference-link/database)
        using the ID specified.\n
        Parameters:
            database_id (str): Identifier for a Notion database, Required\n
        Errors:
            Returns a 404 HTTP response if the page doesn't exist, has been archived,
            or if the integration doesn't have access to the page.\n
            Returns a 400 or a 429 HTTP response if the request exceeds the request limits.
        """
        r = self.session.get(
            self.notion_api + "databases/" + database_id, headers=self.headers
        )
        return r

    def query_a_database(
        self, database_id, filter=None, sorts=None, start_cursor=None, page_size='100'
    ):
        """Gets a list of [Pages](https://developers.notion.com/reference-link/page)
        contained in the database, filtered and ordered according to the filter conditions and sort criteria provided in the request. The response may contain fewer than page_size of results. Filters are similar to [the filters provided in the Notion UI](https://notion.so/notion/Intro-to-databases-fd8cd2d212f74c50954c11086d85997e#a64301249c9d43aa90ac867a35593e4b).
        Filters operate on database properties and can be combined. If no filter is provided, all the pages in the database will be returned with pagination. Sorts are similar to [the sorts provided in the Notion UI](https://notion.so/notion/Intro-to-databases-fd8cd2d212f74c50954c11086d85997e#0eb303043b1742468e5aff2f3f670505).
        Sorts operate on database properties or page timestamps and can be combined. The order of the sorts in the request matter, with earlier sorts taking precedence over later ones.\n
        📘 Database access:
        Integrations can only access databases a user has shared with the bot. Attempting to query a database which is not shared will return an HTTP response with a 404 status code.\n
        See [Pagination](https://developers.notion.com/reference-link/pagination) for details about how to use a cursor to iterate through the list.\n
        Parameters:
            database_id (str): Identifier for a Notion database, Required\n
            filter (obj): When supplied, limits which pages are returned based on the [filter conditions](https://developers.notion.com/reference-link/post-database-query-filter).\n
            sorts (list): When supplied, orders the results based on the provided [sort criteria](https://developers.notion.com/reference-link/post-database-query-sort).\n
            start_cursor (str): When supplied, returns a page of results starting after the cursor provided. If not supplied, this endpoint will return the first page of results.\n
            page_size (int): When supplied, the number of items from the full list desired in the response. Maximum: 100\n
        Errors:
            Returns a 404 HTTP response if the page doesn't exist, has been archived, or if the integration doesn't have access to the page.\n
            Returns a 400 or a 429 HTTP response if the request exceeds the request limits.
        """
        data = None
        if filter or sorts or start_cursor or page_size:
            data = {}
            if filter:
                data["filter"] = filter
            if sorts:
                data["sorts"] = sorts
            if start_cursor:
                data["start_cursor"] = start_cursor
            if page_size:
                data["page_size"] = page_size

        r = self.session.post(
            self.notion_api + "databases/" + database_id + "/query",
            headers=self.headers,
            json=data,
        )
        return r

    # **************************************************************************
    # Sub-Section: Pages
    # **************************************************************************
    def retrieve_a_page(self, page_id):
        """Retrieves a [Page object](https://developers.notion.com/reference-link/page) using the ID specified.\n
        Parameters:
            page_id (str): Identifier for a Notion page, Required\n
        Errors:
            Returns a 404 HTTP response if the page doesn't exist, has been archived, or if the integration doesn't have access to the page.\n
            Returns a 400 or a 429 HTTP response if the request exceeds the request limits.
        """
        r = self.session.get(self.notion_api + "pages/" + page_id, headers=self.headers)
        return r

    def create_a_page(self, parent=None, properties=None, children=None):
        """Creates a new page in the specified database or as a child of an existing page.
        If the parent is a database, the [property values](https://developers.notion.com/reference-link/page-property-value) of the new page in the `properties` parameter must conform to the parent [database's](https://developers.notion.com/reference-link/database) property schema.
        If the parent is a page, the only valid property is `title`.
        The new page may include page content, described as [blocks](https://developers.notion.com/reference-link/block) in the `children` parameter.\n
        📘 Blocks cannot be modified currently,
        Once a block is appended as a child of another block, it cannot be updated or deleted.\n
        Parameters:
            parent (str): A [database parent](https://developers.notion.com/reference/page#database-parent) or [page parent](https://developers.notion.com/reference/page#page-parent)\n
            properties (obj): Property values of this page. The keys are the names or IDs of the [property](https://developers.notion.com/reference-link/database-property) and the values are [property values](https://developers.notion.com/reference-link/page-property-value).\n
            children (list): Page content for the new page as an array of [block objects](https://developers.notion.com/reference-link/block)\n
        Errors:
            Returns a 404 HTTP response if the page doesn't exist, has been archived, or if the integration doesn't have access to the page.\n
            Returns a 400 or a 429 HTTP response if the request exceeds the request limits.
        """
        data = {}
        if parent:
            if "-" in parent:
                data["parent"] = {"page_id": parent}
            else:
                data["parent"] = {"database_id": parent}
        if properties:
            data["properties"] = properties
        if children:
            data["children"] = children

        r = self.session.post(
            self.notion_api + "pages",
            headers=self.headers,
            json=data,
        )
        return r

    def update_a_page(self, page_id, properties=None):
        """Updates [page property values](https://developers.notion.com/reference-link/page-property-value) for the specified page. Properties that are not set via the properties parameter will remain unchanged.
        If the parent is a database, the new property values in the `properties` parameter must conform to the parent [database's](https://developers.notion.com/reference/database) property schema.
        Returns a 200 HTTP response containing the updated [page object](https://developers.notion.com/reference-link/page) on success.
        Requests and responses contains page `properties`, not page content. To fetch page content, use the [retrieve block children](https://developers.notion.com/reference-link/get-block-children) endpoint.
        To append page content, use the [append block children](https://developers.notion.com/reference-link/patch-block-children) endpoint.\n
        Parameters:
            page_id (str): Identifier for a Notion page, Required\n
            properties (obj): Property values of this page. The keys are the names or IDs of the [property](https://developers.notion.com/reference-link/database-property) and the values are [property values](https://developers.notion.com/reference-link/page-property-value).\n
        Errors:
            Returns a 404 HTTP response if the page doesn't exist, has been archived, or if the integration doesn't have access to the page.\n
            Returns a 400 or a 429 HTTP response if the request exceeds the request limits.
        """
        data = None
        if properties:
            data = properties

        r = self.session.patch(
            self.notion_api + "pages/" + page_id,
            headers=self.headers,
            json=data,
        )
        return r

    # **************************************************************************
    # Sub-Section: Blocks
    # **************************************************************************
    def retrieve_block_children(self, block_id, start_cursor=None, page_size='100'):
        """Returns a paginated array of child [block objects](https://developers.notion.com/reference-link/block) contained in the block using the ID specified.
        In order to receive a complete representation of a block, you may need to recursively retrieve the block children of child blocks.
        The response may contain fewer than `page_size` of results.\n
        Parameters:
            block_id (str): Identifier for a [block](https://developers.notion.com/reference-link/block), Required\n
            start_cursor (str): When supplied, returns a page of results starting after the cursor provided. If not supplied, this endpoint will return the first page of results.\n
            page_size (int): When supplied, the number of items from the full list desired in the response. Maximum: 100\n
        Errors:
            Returns a 404 HTTP response if the page doesn't exist, has been archived, or if the integration doesn't have access to the page.\n
            Returns a 400 or a 429 HTTP response if the request exceeds the request limits.
        """
        url = (
            self.notion_api + "blocks/" + block_id + "/children?page_size=" + page_size
        )
        if start_cursor:
            url = url + "&start_cursor=" + start_cursor
        r = self.session.get(url, headers=self.headers)
        return r

    def append_block_children(self, block_id, children):
        """Creates and appends new children blocks to the block using the ID specified. Returns the [Block object](https://developers.notion.com/reference-link/block) which contains the new children.\n
        Parameters:
            block_id (str): Identifier for a [block](https://developers.notion.com/reference-link/block), Required\n
            children (list): Child content to append to a container block as an array of [block objects](https://developers.notion.com/reference-link/block)\n
        Errors:
            Returns a 404 HTTP response if the page doesn't exist, has been archived, or if the integration doesn't have access to the page.\n
            Returns a 400 or a 429 HTTP response if the request exceeds the request limits.
        """
        url = self.notion_api + "blocks/" + block_id + "/children"
        data = {"children": children}
        r = self.session.patch(url, headers=self.headers, json=data)
        return r

    # **************************************************************************
    # Sub-Section: Users
    # **************************************************************************
    def retrieve_a_user(self, user_id):
        """Retrieves a [User](https://developers.notion.com/reference-link/user) using the ID specified.\n
        Parameters:
            user_id (str): Identifier for a Notion user, Required\n
        """
        r = self.session.get(self.notion_api + "users/" + user_id, headers=self.headers)
        return r

    def list_all_users(self, start_cursor=None, page_size='100'):
        """Returns a paginated list of [Users](https://developers.notion.com/reference-link/user) for the workspace. \n
        Parameters:
            start_cursor (str): When supplied, returns a page of results starting after the cursor provided. If not supplied, this endpoint will return the first page of results.\n
            page_size (int): When supplied, the number of items from the full list desired in the response. Maximum: 100\n
        """
        url = self.notion_api + "users?page_size=" + page_size
        if start_cursor:
            url = url + "&start_cursor=" + start_cursor
        r = self.session.get(url, headers=self.headers)
        return r