import api from "@/stores/services/api";
import {defineStore} from "pinia";
import {ref} from "vue";
import type {UserProgress} from "@/models/UserProgress";
import type {Attendance} from "@/models/Attendance";

export const useProgressStore = defineStore('progress', () => {

    const lessonProgress = ref<Dictionary<UserProgress[]>>({});
    const courseProgress = ref<Dictionary<UserProgress[]>>({});

    function setProgress(payload: Dictionary<UserProgress[]>) {
        lessonProgress.value = payload;
    }

    function setCourseProgress(payload: Dictionary<UserProgress[]>) {
        courseProgress.value = payload;
    }

    async function fetchLessonProgressByLessonId(id: number): Promise<UserProgress[]> {
        if (id in lessonProgress.value) {
            return lessonProgress.value[id];
        }

        let answer = {data: {}};
        await api.get('/api/lessonprogress/', {params: {lesson_id: id}})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        const result = answer.data as Array<UserProgress>;
        setProgress({[id]: result})
        return result;
    }

    async function fetchCourseProgressById(id: number): Promise<UserProgress[]> {
        if (id in courseProgress.value) {
            return courseProgress.value[id];
        }
        let answer = {data: {}};
        await api.get('/api/courseprogress/', {params: {course_id: id}})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        const result = answer.data as Array<UserProgress>;
        setCourseProgress({[id]: result})
        return result;
    }

    async function fetchAttendance(id: number): Promise<Dictionary<Attendance[]>> {
        let answer = {data: {}};
        await api.get(`/api/lessonprogress/attendance-by-course/${id}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        return answer.data as Dictionary<Attendance[]>;
    }

    return {
        lessonProgress, courseProgress, setProgress, setCourseProgress, fetchLessonProgressByLessonId,
        fetchCourseProgressById, fetchAttendance
    }
})

export default useProgressStore;
