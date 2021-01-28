class AlignmentMatch():
        
    def __init__(self):
        self.tool_id = 0
        self.process_line_id = 0
        self.align_line_id =0 
        self.process_line = ""
        self.align_line = ""
        self.similarity =0
        self.evaluationMetricName = []
        self.evaluationMetricValue = []
        super().__init__()

    def addEvalationMetricResult(self, metricName, metricValue):
        self.evaluationMetricName.append(metricName)
        self.evaluationMetricValue.append(metricValue)

    def getHeaders(self):
        return [
            "tool id",
            "org sent id",
            "trg sent id",
            "original",
            "target", 
            "similarity"
        ] + self.evaluationMetricName

    def getValues(self):
        return [
            self.tool_id,
            self.process_line_id,
            self.align_line_id, 
            self.process_line,
            self.align_line,
            self.similarity
        ] + self.evaluationMetricValue