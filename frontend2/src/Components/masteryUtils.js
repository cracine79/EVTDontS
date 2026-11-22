// Topic scores shown to students: the server's mastery score (recent answers count more, thin data
// is pulled toward 50%; see backend/mastery.py), falling back to the all-time % for older data.
export const masteryPercent = (topic) => {
    if (!topic) return 0
    if (topic.mastery_percent !== undefined && topic.mastery_percent !== null) return topic.mastery_percent
    return topic.percent_correct || 0
}

export const isReviewDue = (topic) => !!(topic && topic.review_due)
