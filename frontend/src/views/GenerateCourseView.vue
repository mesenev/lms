<template>
  <div class="course-generator">
    <div class="generator-card">
      <h2 class="title">Генератор курсов</h2>
      
      <div class="form-group">
        <label for="courseName" class="label">Название курса</label>
        <input
          id="courseName"
          v-model="courseName"
          type="text"
          class="input"
          placeholder="Например: Введение в Python, Основы маркетинга..."
          @keyup.enter="generateCourse"
        />
      </div>
      
      <button 
        @click="generateCourse" 
        :disabled="!courseName.trim() || isLoading"
        class="generate-btn"
        :class="{ 'loading': isLoading }"
      >
        <span v-if="!isLoading">✨ Сгенерировать курс</span>
        <span v-else>
          <span class="spinner"></span>
          Генерация...
        </span>
      </button>
      
      <!-- Отображение ошибки -->
      <div v-if="error" class="error-message">
        ⚠️ {{ error }}
      </div>
      
            
      <!-- Счетчик символов -->
      <div class="character-counter" v-if="courseName">
        {{ courseName.length }}/100
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/stores/services/api'
import { ref, watch } from 'vue'

// Определение emits
const emit = defineEmits(['course-generated'])

// Реактивные данные
const courseName = ref('')
const isLoading = ref(false)
const error = ref(null)
const generatedCourse = ref(null)

// Валидация и ограничение длины названия
watch(courseName, (newVal) => {
  // Ограничиваем длину названия
  if (newVal.length > 100) {
    courseName.value = newVal.slice(0, 100)
  }
  // Очищаем ошибку при изменении ввода
  if (error.value) {
    error.value = null
  }
})

// Генерация курса
const generateCourse = async () => {
  // Валидация
  if (!courseName.value.trim()) {
    error.value = 'Пожалуйста, введите название курса'
    return
  }
  
  if (courseName.value.length < 3) {
    error.value = 'Название курса должно содержать минимум 3 символа'
    return
  }
  
  error.value = null
  isLoading.value = true
  
  try {
    await api.post('generate-course', {"courseName": courseName.value})   
  } catch (err) {
    error.value = 'Ошибка при генерации курса. Пожалуйста, попробуйте снова.'
    console.error('Generation error:', err)
  } finally {
    isLoading.value = false
  }
}

// Очистка результата
const clearResult = () => {
  generatedCourse.value = null
  courseName.value = ''
  error.value = null
}
</script>

<style scoped>
.course-generator {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

.generator-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 25px;
}

.label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #4a5568;
  font-size: 14px;
}

.input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.generate-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.generate-btn.loading {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  background-color: #fed7d7;
  color: #c53030;
  padding: 12px;
  border-radius: 8px;
  margin-top: 20px;
  border-left: 4px solid #c53030;
}

.result-section {
  margin-top: 30px;
  background: #f7fafc;
  border-radius: 12px;
  overflow: hidden;
  animation: slideIn 0.5s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-header {
  background: #edf2f7;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
}

.result-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 18px;
}

.clear-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #718096;
  transition: color 0.3s ease;
}

.clear-btn:hover {
  color: #e53e3e;
}

.result-content {
  padding: 20px;
}

.result-content h4 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 20px;
}

.course-description {
  background: white;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #4299e1;
}

.course-description p {
  margin: 0;
  line-height: 1.6;
  color: #4a5568;
}

.course-modules {
  margin-bottom: 20px;
}

.course-modules h5 {
  color: #2d3748;
  margin: 0 0 12px 0;
  font-size: 16px;
}

.course-modules ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.course-modules li {
  background: white;
  margin-bottom: 10px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.course-modules li strong {
  color: #2c3e50;
  display: block;
  margin-bottom: 5px;
}

.course-duration {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.badge {
  background: #e2e8f0;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  color: #4a5568;
}

.character-counter {
  text-align: right;
  font-size: 12px;
  color: #a0aec0;
  margin-top: 8px;
}

@media (max-width: 640px) {
  .generator-card {
    padding: 20px;
  }
  
  .title {
    font-size: 24px;
  }
  
  .input {
    font-size: 14px;
  }
}
</style>