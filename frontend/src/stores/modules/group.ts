import { defineStore } from "pinia";
import { computed, ref } from "vue";
import type { GroupModel } from "@/models/GroupModel";
import api from "@/stores/services/api";

export const useGroupStore = defineStore('course', () => {
    const groupsByCourse = ref<Dictionary<GroupModel[]>>([]);

    const newGroup = computed(() => {
        return {
            id: NaN,
            teachers: [],
            students: [],
        } as GroupModel
    });

    function setGroups(payload: Dictionary<GroupModel[]>) {
        groupsByCourse.value = {...groupsByCourse.value, ...payload};
    }

    async function fetchGroupsByCourseId(id: number): Promise<Array<GroupModel>> {
        let answer = { data: {} };
        await api.get('/api/group/', {params: {course_id: id}})
        .then(response => {
            answer = response;
            setGroups({[id]: answer.data})
        })
        .catch(error => {
            console.log(error);
        })
        return answer.data as Array<GroupModel>;
    }

    return { groupsByCourse, newGroup, setGroups, fetchGroupsByCourseId }
});

export default useGroupStore;