// import { useState, useEffect } from 'react'

// export function useFetch(url) {
//   const [data, setData] = useState({})
//   const [isLoading, setLoading] = useState(true)
//   const [error, setError] = useState(false)

//   useEffect(() => {
//     if (!url) return
//     setLoading(true)
//     async function fetchData() {
//       try {
//         const response = await fetch(url)
//         const data = await response.json()
//         console.log(data)
//         setData(data)
//       } catch (err) {
//         console.log(err)
//         setError(true)
//       } finally {
//         setLoading(false)
//       }
//     }
//     fetchData()
//   }, [url])
//   return { data, isLoading, error }
// }

// const baseURL = 'http://localhost/api/'

// export function useFetchVolumes() {
//   const url = `${baseURL}/datamodel/volumes`
//   const [volumes, setVolumes] = useState({})
//   const [isLoadingVolumes, setLoadingVolumes] = useState(true)
//   const [errorLoadingVolumes, setErrorLoadingVolumes] = useState(false)

//   useEffect(() => {
//     if (!url) return
//     setLoadingVolumes(true)
//     async function fetchData() {
//       try {
//         const response = await fetch(url)
//         const data = await response.json()
//         console.log(data)
//         setVolumes(data)
//       } catch (err) {
//         console.log(err)
//         setErrorLoadingVolumes(true)
//       } finally {
//         setLoadingVolumes(false)
//       }
//     }
//     fetchData()
//   }, [url])
//   return { volumes, isLoadingVolumes, errorLoadingVolumes }
// }

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
