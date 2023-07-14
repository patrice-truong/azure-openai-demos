from src.openai.service import OpenAIService

import os

class CosmosDBforGremlinService:

    def __init__(self, gremlin_client):
        self.gremlin_client = gremlin_client

    def print_status_attributes(self, result):
        # This logs the status attributes returned for successful requests.
        # See list of available response status attributes (headers) that Gremlin API can return:
        #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
        #
        # These responses includes total request units charged and total server latency time.
        # 
        # IMPORTANT: Make sure to consume ALL results returend by cliient tothe final status attributes
        # for a request. Gremlin result are stream as a sequence of partial response messages
        # where the last response contents the complete status attributes set.
        #
        # This can be 
        print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))
        
    # check if the Cosmos DB service is running OK
    def service_check(self):
        try:
            self.execute_query("g.V().count()")
            return "Cosmos DB for Gremlin service is running OK"
        except Exception as e:
            return f"Cosmos DB for Gremlin service error: {str(e)}"

    def count(self):
        try:
            count = self.execute_query("g.V().count()")
            return count
        except Exception as e:
            return f"Cosmos DB for Gremlin service error: {str(e)}"

    def execute_query(self, query):
        print("\n> {0}".format(query))
        callback = self.gremlin_client.submitAsync(query)
        if callback.result() is not None:
            result = callback.result().all().result()
        else:
            print("Something went wrong with this query: {0}".format(query))

        print("\n")
        self.print_status_attributes(callback.result())
        print("\n")
        return result