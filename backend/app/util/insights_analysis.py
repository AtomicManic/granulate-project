class InsightAnalysis:
    @staticmethod
    def analyze_insights(data: dict) -> dict:
        """Analyze the given insights data and return a formatted response."""

        sugg_ppm, cur_ppm = 0, 0
        insights_response = {
            'id': data['id'],
            'customer_name': data['customerName'],
            'vms_rec': []
        }

        vms = data['vms']
        for vm in vms:
            # create insights dictionary for single vm
            current = vm["vmSizeCurrent"]
            suggestions = vm["vmSizeSuggested"]
            insight_vm = {
                'id': vm["id"],
                'name': vm["name"],
                'tag': vm["tags"]["Name"],
                'tenancy': vm["tenancy"],
                'os': vm["operatingSystem"],
                'general': InsightAnalysis.analyze_general(
                    current, suggestions)
            }

            # analyze best monthly payment for vm
            current_cheap, sugg_cheap, curr_tag, sugg_tag = InsightAnalysis.analyze_monthly_payment(
                current["pricePerMonth"], suggestions["pricePerMonth"])

            # Insert bmp to vm dictionary
            insight_vm['pricing'] = {'current': {'price': current_cheap, 'tag': curr_tag}, 'suggested': {
                'price': sugg_cheap, 'tag': sugg_tag}}

            # calculate overall current payment and suggested payment
            if sugg_cheap:
                sugg_ppm += sugg_cheap
            if current_cheap:
                cur_ppm += current_cheap

            # insert vm insights to response
            insights_response['vms_rec'].append(insight_vm)

        # Add current and suggested overall payment to response
        insights_response['pricing'] = {'prev': cur_ppm, 'suggested': sugg_ppm}
        return insights_response

    @staticmethod
    def analyze_general(current, suggested):
        """Analyze and return general insights for a given VM."""

        # function to get the attribute if insights and current state are not the same
        def get_dict_if_different(current_val, suggested_val, key):
            return {key: {'prev': current_val, 'suggested': suggested_val}} if current_val != suggested_val else {}

        # if there are no suggestions for vm, give an instruction to delete it
        if not suggested["instanceFullName"]:
            return {'toDelete': True}

        # Make the general changes section dictionary
        general = {
            'instance_size': {'prev': current["instanceSize"], 'suggested': suggested["instanceSize"]},
            **get_dict_if_different(current["instanceCapabilities"]["memoryGB"], suggested["instanceCapabilities"]["memoryGB"], 'memory_GB'),
            **get_dict_if_different(current["instanceCapabilities"]["maxResourceVolumeMB"], suggested["instanceCapabilities"]["maxResourceVolumeMB"], 'max_resouce_volume'),
            **get_dict_if_different(current["location"], suggested["location"], 'location'),
        }

        return general

    @staticmethod
    def get_cheap_and_tag(ppm) -> tuple:
        """Return the cheapest price and its corresponding tag."""

        if ppm['onDemand'] != None and ppm['reservedOneYear'] != None and ppm['onDemand'] <= ppm['reservedOneYear']:
            return ppm['onDemand'], 'onDemand'
        else:
            return ppm['reservedOneYear'], 'reservedOneYear'

    @staticmethod
    def analyze_monthly_payment(ppm_current, ppm_suggested):
        """Analyze and return the best monthly payment and its tag."""

        current_cheap, curr_tag = InsightAnalysis.get_cheap_and_tag(
            ppm_current)
        sugg_cheap, sugg_tag = InsightAnalysis.get_cheap_and_tag(ppm_suggested)

        return current_cheap, sugg_cheap, curr_tag, sugg_tag
