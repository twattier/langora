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

const baseURL = 'http://localhost/api/'

export function useFetchKnowledge() {
  const url = `${baseURL}/knowledge`
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

  export function useFetchSimilarities(query) {
    const url = `${baseURL}/similarities?query=${query}`
    const [similarities, setSimilarities] = useState({})
    const [isLoadingSimilarities, setLoadingSimilarities] = useState(true)
    const [errorLoadingSimilarities, setErrorLoadingSimilarities] = useState(false)
  
    useEffect(() => {
      if (!url) return      
      if(query===undefined || query==='') return      
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
    const url = `${baseURL}/genai?query=${query}`
    const [resultGenAI, setResultGenAI] = useState({})
    const [isLoadingResultGenAI, setLoadingResultGenAI] = useState(true)
    const [errorLoadingResultGenAI, setErrorLoadingResultGenAI] = useState(false)
  
    useEffect(() => {
      if (!url) return
      if(query===undefined || query==='') return
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

// export function useFetchVolumesImport() {
//   const url = `${baseURL}/backend/volumes/import`
//   const [volumesImport, setVolumesImport] = useState({})
//   const [isLoadingVolumesImport, setLoadingVolumesImport] = useState(true)
//   const [errorLoadingVolumesImport, setErrorLoadingVolumesImport] = useState(false)

//   useEffect(() => {
//     if (!url) return
//     setLoadingVolumesImport(true)
//     async function fetchData() {
//       try {
//         const response = await fetch(url)
//         const data = await response.json()
//         console.log(data)
//         setVolumesImport(data)
//       } catch (err) {
//         console.log(err)
//         setErrorLoadingVolumesImport(true)
//       } finally {
//         setLoadingVolumesImport(false)
//       }
//     }
//     fetchData()
//   }, [url])
//   return { volumesImport, isLoadingVolumesImport, errorLoadingVolumesImport }
// }

// export function apiImport(type, volumeId) {
//   const action = type === "PDF" ? "import_books" : "import_wiki"
//   const url = `${baseURL}/tasks/${action}/${volumeId}`
//   fetch(url, { method: 'GET' })
//     .then(window.location.reload())
// }

// // export function useFetchTasks() {
// //   const url = `${baseURL}/tasks/status/all`
// //   const [tasks, setTasks] = useState({})
// //   const [isLoadingTasks, setLoadingTasks] = useState(true)
// //   const [errorLoadingTasks, setErrorLoadingTasks] = useState(false)

// //   useEffect(() => {
// //     if (!url) return
// //     setLoadingTasks(true)
// //     async function fetchData() {
// //       try {
// //         const response = await fetch(url)
// //         const data = await response.json()
// //         console.log(data)
// //         setTasks(data)
// //       } catch (err) {
// //         console.log(err)
// //         setErrorLoadingTasks(true)
// //       } finally {
// //         setLoadingTasks(false)
// //       }
// //     }
// //     fetchData()
// //   }, [url])
// //   return { tasks, isLoadingTasks, errorLoadingTasks }
// // }

// // export function useFetchImportTasks() {
// //   const { tasks, isLoadingTasks, errorLoadingTasks } = useFetchTasks()
// //   if (isLoadingTasks || errorLoadingTasks || !tasks)
// //     return { tasks, isLoadingTasks, errorLoadingTasks }

// //   const list = tasks.filter(t=>t.desc.is_import)
// //   return {list, isLoadingTasks, errorLoadingTasks}
// // }

// // export function useFetchVolumeImportTasks(volumeId) {
// //   const { tasks, isLoadingTasks, errorLoadingTasks } = useFetchImportTasks()
// //   if (isLoadingTasks || errorLoadingTasks || !tasks)
// //     return { tasks, isLoadingTasks, errorLoadingTasks }

// //   const listPDF = tasks.filter(t=>t.desc.import_type === "PDF" && t.desc.import_volume === volumeId)
// //   const listWiki = tasks.filter(t=>t.desc.import_type === "Wiki" && t.desc.import_volume === volumeId)
// //   return { listPDF, listWiki, isLoadingTasks, errorLoadingTasks }
// // }

// // export function useFetchTask(taskId) {
// //   const url = `${baseURL}/tasks/${taskId}`
// //   const [taskPerId, setTaskPerId] = useState({})
// //   const [isLoadingTaskPerId, setLoadingTaskPerId] = useState({})
// //   const [errorLoadingTaskPerId, setErrorLoadingTaskPerId] = useState({})

// //   useEffect(() => {
// //     if (!url) return
// //     setLoadingTaskPerId({...isLoadingTaskPerId, taskId : true})
// //     async function fetchData() {
// //       try {
// //         const response = await fetch(url)
// //         const data = await response.json()
// //         console.log(data)
// //         setTaskPerId({...taskPerId, taskId : data})
// //       } catch (err) {
// //         console.log(err)
// //         setErrorLoadingTaskPerId({...errorLoadingTaskPerId, taskId : true})
// //       } finally {
// //         setLoadingTaskPerId({...isLoadingTaskPerId, taskId : false})
// //       }
// //     }
// //     fetchData()
// //   }, [url, taskPerId, isLoadingTaskPerId, errorLoadingTaskPerId])
// //   return { taskPerId, isLoadingTaskPerId, errorLoadingTaskPerId }
// // }
