class Store:

    ##########################################################################
    # API methods
    ##########################################################################

    @classmethod
    def products(cls, categories=None, extra_args=None,
                 discover_urls_concurrency=3,
                 products_for_url_concurrency=3, use_async=False):
        extra_args = cls._extra_args_with_preflight(extra_args)

        discovered_entries = cls.discover_entries_for_categories(
            categories=categories,
            extra_args=extra_args,
            discover_urls_concurrency=discover_urls_concurrency,
            use_async=use_async
        )

        print(
            discovered_entries,
            extra_args,
            products_for_url_concurrency,
            use_async
        )

        return cls.products_for_urls(
            discovered_entries,
            extra_args=extra_args,
            products_for_url_concurrency=products_for_url_concurrency,
            use_async=use_async
        )

    @classmethod
    def products_for_urls(cls, discovered_entries, extra_args=None,
                          products_for_url_concurrency=None,
                          use_async=True):
        print(
            discovered_entries,
            extra_args,
            products_for_url_concurrency,
            use_async
        )

        products = []
        discovery_urls_without_products = []

        for entry_url, entry_metadata in discovered_entries.items():
            print(
                'aaaaaaaaaaaaaaa',
                entry_url,
                entry_metadata['category'],
                extra_args
            )
            retrieved_products = cls.products_for_url(
                entry_url,
                entry_metadata['category'],
                extra_args)

            print(retrieved_products)

            for product in retrieved_products:
                if not product.positions:
                    product.positions = entry_metadata['positions']
                products.append(product)

            if not retrieved_products:
                discovery_urls_without_products.append(entry_url)

        return {
            'products': products,
            'discovery_urls_without_products': discovery_urls_without_products
        }

    @classmethod
    def _extra_args_with_preflight(cls, extra_args=None):
        preflight_args = {
            'preflight_done': True
        }
        return preflight_args

    @classmethod
    def discover_entries_for_categories(cls, categories=None,
                                        extra_args=None,
                                        discover_urls_concurrency=None,
                                        use_async=True):
        return {'Notebook': {'positions': {}, 'category': 'Notebook', 'category_weight': 1}}
