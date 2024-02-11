import { useState, useEffect } from 'react'

export function useFetch(url) {
  const [data, setData] = useState({})
  const [isLoading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    if (!url) return
    setLoading(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        console.log(data)
        setData(data)
      } catch (err) {
        console.log(err)
        setError(true)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [url])
  return { data, isLoading, error }
}

export const baseURL = 'http://localhost/api'

export function useFetchKnowledge() {
  const url = `${baseURL}/knowledges`
  const [knowledge, setknowledge] = useState({})
  const [isLoadingknowledge, setLoadingknowledge] = useState(true)
  const [errorLoadingknowledge, setErrorLoadingknowledge] = useState(false)

  useEffect(() => {
    if (!url) return
    setLoadingknowledge(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setknowledge(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingknowledge(true)
      } finally {
        setLoadingknowledge(false)
      }
    }
    fetchData()
  }, [url])
  return { knowledge, isLoadingknowledge, errorLoadingknowledge }
}

export function useFetchTopics() {
  const url = `${baseURL}/topics`
  const [topics, setTopics] = useState({})
  const [isLoadingTopics, setLoadingTopics] = useState(true)
  const [errorLoadingTopics, setErrorLoadingTopics] = useState(false)

  useEffect(() => {
    if (!url) return
    setLoadingTopics(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setTopics(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingTopics(true)
      } finally {
        setLoadingTopics(false)
      }
    }
    fetchData()
  }, [url])
  return { topics, isLoadingTopics, errorLoadingTopics }
}

export function useFetchTopSources() {
  const url = `${baseURL}/sources`
  const [topSources, setTopSources] = useState({})
  const [isLoadingTopSources, setLoadingTopSources] = useState(true)
  const [errorLoadingTopSources, setErrorLoadingTopSources] = useState(false)

  useEffect(() => {
    if (!url) return
    setLoadingTopSources(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setTopSources(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingTopSources(true)
      } finally {
        setLoadingTopSources(false)
      }
    }
    fetchData()
  }, [url])
  return { topSources, isLoadingTopSources, errorLoadingTopSources }
}

export function useFetchTopSearches() {
  const url = `${baseURL}/searches`
  const [topSearches, setTopSearches] = useState({})
  const [isLoadingTopSearches, setLoadingTopSearches] = useState(true)
  const [errorLoadingTopSearches, setErrorLoadingTopSearches] = useState(false)

  useEffect(() => {
    if (!url) return
    setLoadingTopSearches(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setTopSearches(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingTopSearches(true)
      } finally {
        setLoadingTopSearches(false)
      }
    }
    fetchData()
  }, [url])
  return { topSearches, isLoadingTopSearches, errorLoadingTopSearches }
}

export function useFetchSearch(searchId) {
  const url = `${baseURL}/searches/${searchId}`
  const [search, setSearch] = useState({})
  const [isLoadingSearch, setLoadingSearch] = useState(true)
  const [errorLoadingSearch, setErrorLoadingSearch] = useState(false)

  useEffect(() => {
    if (!url) return
    setLoadingSearch(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setSearch(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingSearch(true)
      } finally {
        setLoadingSearch(false)
      }
    }
    fetchData()
  }, [url])
  return { search, isLoadingSearch, errorLoadingSearch }
}

export function useFetchSimilarities(type, query) {
  const url = `${baseURL}/${type}/similarities?query=${query}`
  const [similarities, setSimilarities] = useState({})
  const [isLoadingSimilarities, setLoadingSimilarities] = useState(true)
  const [errorLoadingSimilarities, setErrorLoadingSimilarities] =
    useState(false)

  useEffect(() => {
    if (!url) return
    if (query === undefined || query === '') return
    setLoadingSimilarities(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setSimilarities(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingSimilarities(true)
      } finally {
        setLoadingSimilarities(false)
      }
    }
    fetchData()
  }, [url, query])
  return { similarities, isLoadingSimilarities, errorLoadingSimilarities }
}

export function useFetchGenAI(query) {
  const url = `${baseURL}/knowledges/genai?query=${query}`
  const [resultGenAI, setResultGenAI] = useState({})
  const [isLoadingResultGenAI, setLoadingResultGenAI] = useState(true)
  const [errorLoadingResultGenAI, setErrorLoadingResultGenAI] = useState(false)

  useEffect(() => {
    if (!url) return
    if (query === undefined || query === '') return
    setLoadingResultGenAI(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setResultGenAI(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingResultGenAI(true)
      } finally {
        setLoadingResultGenAI(false)
      }
    }
    fetchData()
  }, [url, query])
  return { resultGenAI, isLoadingResultGenAI, errorLoadingResultGenAI }
}

export function useFetchTasks(autoRefresh) {
  const url = `${baseURL}/tasks/status/pending`
  const [tasks, setTasks] = useState({})
  const [isLoadingTasks, setLoadingTasks] = useState(true)
  const [errorLoadingTasks, setErrorLoadingTasks] = useState(false)

  useEffect(() => {
    if (!url) return
    setLoadingTasks(true)
    async function fetchData() {
      try {
        const response = await fetch(url)
        const data = await response.json()
        setTasks(data)
      } catch (err) {
        console.log(err)
        setErrorLoadingTasks(true)
      } finally {
        setLoadingTasks(false)
      }
    }
    fetchData()
    if (autoRefresh) {
      const intervalId = setInterval(() => {
        fetchData() // Fetch data every 5 seconds
      }, 5000)
      return () => clearInterval(intervalId);
    }
  }, [url, autoRefresh])
  return { tasks, isLoadingTasks, errorLoadingTasks }
}
