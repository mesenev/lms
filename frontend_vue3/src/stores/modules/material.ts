import api from '@/stores/services/api';
import {computed, ref} from "vue";
import type {MaterialModel} from "@/models/MaterialModel";
import type {AttachmentModel} from "@/models/Attachment";
import {defineStore} from "pinia";

export const useMaterialStore = defineStore('material', () => {

    const _materials = ref<Dictionary<MaterialModel[]>>({});

    const getNewMaterial = computed(() => {
        return {
            id: NaN,
            lesson: NaN,
            name: '',
            content_type: '',
            content: '',
            is_teacher_only: false,
        };
    })

    const _currentMaterial = ref<MaterialModel>({...getNewMaterial.value});
    const _currentAttachments = ref<Array<AttachmentModel>>([]);

    const currentMaterial = computed(() => {
        return _currentMaterial.value;
    })

    const currentAttachments = computed(() => {
        return _currentAttachments.value;
    })

    const currentMaterialType = computed(() => {
        return _currentMaterial.value.content_type;
    })

    const currentMaterialUrl = computed(() => {
        if (currentMaterialType.value === 'video') {
            return _currentMaterial.value.content;
        }
        return undefined;
    })

    function setMaterials(payload: Dictionary<MaterialModel[]>) {
        _materials.value = payload;
    }

    function setCurrentMaterial(material: MaterialModel) {
        _currentMaterial.value = material;
    }

    async function patchMaterialVisibility(params: { is_teacher_only: boolean; id: number }): Promise<MaterialModel> {
        let answer = {data: {}};
        await api.patch(`/api/material/${params.id}/`, {...params})
            .then(response => {
                answer = response;
            })
            .catch(error => {
                console.log(error);
            });
        setCurrentMaterial(answer.data as MaterialModel);
        return answer.data as MaterialModel;
    }

    async function fetchMaterials() {
        await api.get('/api/material/')
            .then(response => {
                setMaterials(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    async function fetchMaterialById(id: number): Promise<MaterialModel> {
        let answer = {data: {}};
        await api.get(`/api/material/${id}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            });
        return answer.data as MaterialModel;
    }

    async function fetchMaterialsByLessonId(id: number): Promise<MaterialModel[]> {
        if (id in _materials.value) {
            return _materials.value[id];
        }

        let answer = {data: {}};
        await api.get('/api/material/', {params: {lesson_id: id}})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            });
        const result = answer.data as Array<MaterialModel>;
        setMaterials({[id]: result});
        return result;
    }

    function setCurrentAttachments(attachments: AttachmentModel[]) {
        _currentAttachments.value = attachments;
    }

    async function createAttachment(attachment: FormData) {
        await api.post('/api/attachments/', attachment);
    }

    async function deleteAttachment(attachment_id: number) {
        await api.delete(`/api/attachments/${attachment_id}/`).then(response => {
                fetchAttachmentsByMaterialId(currentMaterial.value.id);
            }
        );
    }

    async function fetchAttachmentsByMaterialId(material_id: number) {
        let answer = {data: {}};
        await api.get('/api/attachments/', {params: {material_id: material_id}})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            });
        const result = answer.data as Array<AttachmentModel>;
        setCurrentAttachments(result);
    }

    return {
        getNewMaterial, fetchMaterials, currentMaterial, currentAttachments, currentMaterialType,
        currentMaterialUrl, setMaterials, setCurrentMaterial, patchMaterialVisibility, fetchMaterialById,
        fetchMaterialsByLessonId, setCurrentAttachments, createAttachment, deleteAttachment,
        fetchAttachmentsByMaterialId
    }
})

export default useMaterialStore;
