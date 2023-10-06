import api from '@/stores/services/api'
import * as types from "@/models/LogEventModel";
import {defineStore} from "pinia";
import {computed} from "vue";
import type {LogEventModel} from "@/models/LogEventModel";

export const useLogEventStore = defineStore('logEvent', () => {

    const getNewLogEventMessage = computed(() => {
        return {
            id: NaN, type: types.TYPE_MESSAGE, student: NaN, problem: NaN, data: {},
        }
    })

    async function fetchLogEventsByProblemAndStudentIds(
        data: { problem: number; student: number; limit: number; offset: number }
    ):
        Promise<Array<LogEventModel>> {
        let answer = {};
        await api.get('/api/logevents/', {
            params: data,
        }).then(response => {
            answer = response.data.results;
        })
            .catch(error => {
                console.error(error);
            })
        return (answer as Array<LogEventModel>)
    }

    async function deleteEvent(id: number) {
        let answer = {};
        await api.delete(`/api/logevents/${id}/`).then(
            response => {
                answer = response.data;
            },
        ).catch(reason => {
            //
        });
        return answer;
    }

    async function createLogEvent(event: LogEventModel): Promise<LogEventModel | undefined> {
        let answer: { id?: number } = {};
        delete (event as { id?: number }).id;
        await api.post('/api/logevents/', event).then(
            response => answer = response.data as LogEventModel,
        ).catch(response => console.log('error creating event', response))
        if (answer.id !== undefined)
            return answer as LogEventModel;
        return undefined;
    }

    return {
        getNewLogEventMessage, fetchLogEventsByProblemAndStudentIds, deleteEvent, createLogEvent
    }
})

export default useLogEventStore;
