import parcels
class DataManager:
    def get_area(chrom):
        area = 0
        for x in chrom:
            area += x.area
        return area
    def to_json(chrom, container_type):
        dict = [{
                "Container_Type": container_type,
                "Area" : DataManager.get_area(chrom),
                "Container" : [
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    []
            ]
            }
        ]
        row_cnt = -1
        sum_weight = 0
        weight_sections = []
        sum_width = 0
        for x, j in enumerate(chrom):
            if x % 3 == 0:
                if sum_width > parcels.Info.get_container_info(container_type)[0]:
                    print(f"Row#{row_cnt}=> overwidth")
                sum_width = 0
                row_cnt += 1
            dict[0]['Container'][row_cnt].append(j.name)
            for y, z in j.weight_each.items():
                for o in z:
                    sum_weight += o
            if x == 10 or x == 21 or x == 32:
                weight_sections.append(sum_weight)
                sum_weight = 0
            sum_width += j.width
        print(sum(weight_sections))
        # for i in weight_sections:
        #     print(round((i / sum(weight_sections) * 100), 2))
        dict[0]['Weight'] = sum(weight_sections)
        return dict