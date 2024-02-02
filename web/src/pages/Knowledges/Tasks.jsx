import * as React from 'react'
import { useState } from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import { DataGrid } from '@mui/x-data-grid'
import { useGridApiRef } from '@mui/x-data-grid'
import CircularProgress from '@mui/material/CircularProgress'
import Button from '@mui/material/Button'

import { ContentBox } from '../../utils/style/component'
import NavBar from '../../components/Sources/NavBar'
import { baseURL, useFetchTasks } from '../../utils/hooks'

export default function Tasks() {
  const { tasks, isLoadingTasks, errorLoadingTasks } = useFetchTasks()
  if (errorLoadingTasks) {
    return <span>Impossible to load the liste of Tasks</span>
  } 
  // else if (!isLoadingTasks && tasks !== undefined) {
  //   const res = []
  //   tasks.forEach((element) => {
  //     const row = {}
  //     res.push(row)
  //   })
  //   setRows(res)
  // }

  const columns = [
    { field: 'enqueued', type:'dateTime', headerName: 'Created', width: 150 },
    { field: 'status', headerName: 'Status', width: 90 },
    { field: 'start', type:'dateTime', headerName: 'Started', width: 150 },
    { field: 'name', headerName: 'Task', flex: 2},
    { field: 'item_label', headerName: 'Item', flex: 3},
  ]

  const apiUpdate = () => {
    const url = `${baseURL}/tasks/knowledge/update`
    fetch(url, { method: 'GET' })
      .then(window.location.reload())
  }

  return (
    <Stack>
      <NavBar selected="tasks" />
      <ContentBox>
        <Stack>
        {isLoadingTasks ? (
          <CircularProgress />
        ) : tasks.length === 0 ? (
          <Box> No task in progress</Box>
        ) : (
          <DataGrid
            rows={tasks}
            columns={columns}
            initialState={{
              pagination: {
                paginationModel: {
                  pageSize: 10,
                },
              },
            }}
            pageSizeOptions={[10]}
            checkboxSelection
            disableRowSelectionOnClick
          />
        )}
        <Box display="flex-end">
            <Button onClick={apiUpdate}>Fill Knowledge Base</Button>
        </Box>
        </Stack>
      </ContentBox>
    </Stack>
  )
}
