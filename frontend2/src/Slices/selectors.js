import { createSelector } from "@reduxjs/toolkit";

const selectChapters = (state) => state.chapters.byId;
const selectUserProgress = (state) => state.userChapters.byId;

// Combined selector for user-associated chapters
export const selectUserChapters = createSelector(
  [selectChapters, selectUserProgress],
  (chapters, userProgress) => {
    return Object.keys(userProgress).map((chapterId) => ({
      ...chapters[chapterId],
      ...userProgress[chapterId],
    }));
  }
);
