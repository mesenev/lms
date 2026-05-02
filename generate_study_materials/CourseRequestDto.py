class CourseRequestDto:

    courseId = 0
    topic = ""
    courseType = ""
    difficultyLevel = 0
    createdBy = 0

    def __init__(self, courseId, topic, courseType, difficultyLevel, createdBy):
        self.courseId = courseId
        self.topic = topic
        self.courseType = courseType
        self.difficultyLevel = difficultyLevel
        self.createdBy = createdBy
