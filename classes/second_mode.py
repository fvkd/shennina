import sys
import pandas as pd
import config
sys.path.append(config.PROJECT_PATH + "/classes/")
import utils
import operator


class MemoryModel(object):
    def save(self, result):
        utils.save_file(config.SECOND_BRAIN_NAME, result)

    def get_prediction(self, result, service):
        try:
            service_data = result[service]
            sorted_data = sorted(service_data.items(), key=operator.itemgetter(1))
            return [item[0] for item in sorted_data]
        except Exception:  # Not found
            return []

    def play(self, service):
        results = self.load_brain()
        service = service.lower().replace(" ", "")
        service_data = self.get_prediction(results, service)
        return service_data

    def init_brain(self, result={}):
        exploit_data = pd.read_csv(config.SUPERVISOD_CSV_FILE)

        # Optimize: Normalize service names using vectorized string operations
        exploit_data['service'] = exploit_data['service'].str.lower().str.replace(" ", "")

        # Group by service and exploit to count occurrences efficiently
        counts = exploit_data.groupby(['service', 'exploit']).size()

        # Iterate over the aggregated counts to update the result dictionary
        for (service_name, exploit_name), count in counts.items():
            if service_name in result:
                if exploit_name in result[service_name]:
                    result[service_name][exploit_name] += count
                else:
                    result[service_name][exploit_name] = count
            else:
                result[service_name] = {exploit_name: count}

        self.save(result)
        return result

    def resume_brain(self):
        return utils.load_file(config.SECOND_BRAIN_NAME)

    def load_brain(self):
        result = {}
        if utils.check_if_filename_exists(config.SECOND_BRAIN_NAME):
            result = self.resume_brain()
        return self.init_brain(result)
