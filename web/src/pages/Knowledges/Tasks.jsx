import * as React from 'react'
import moment from 'moment'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import { DataGrid } from '@mui/x-data-grid'
import CircularProgress from '@mui/material/CircularProgress'
import Switch from '@mui/material/Switch'

import { ContentBox, ActionButton } from '../../utils/style/component'
import NavBar from '../../components/Knowledges/NavBar'
import { baseURL, useFetchTasks } from '../../utils/hooks'

export default function Tasks() {
  const [autoRefresh, setAutoRefresh] = React.useState(false)

  const { tasks, isLoadingTasks, errorLoadingTasks } =
    useFetchTasks(autoRefresh)
  if (errorLoadingTasks) {
    return <span>Impossible to load the liste of Tasks</span>
  }

  const columns = [
    {
      field: 'enqueued_at',
      type: 'datetime',
      headerName: 'Created',
      width: 150,
      valueFormatter: (params) =>
        moment(params?.value).format('YYYY/MM/DD hh:mm'),
    },
    { field: 'status', headerName: 'Status', width: 90 },
    {
      field: 'start_at',
      type: 'datetime',
      headerName: 'Started',
      width: 150,
      valueFormatter: (params) => {
        if (params.value === null) return ''
        else moment(params.value).format('YYYY/MM/DD hh:mm')
        // return moment(params.value).fromNow()
      },
    },
    { field: 'name', headerName: 'Task', flex: 1 },
    { field: 'item_label', headerName: 'Item', flex: 3 },
  ]

  const apiUpdate = () => {
    const url = `${baseURL}/tasks/knowledge/update`
    fetch(url, { method: 'GET' }).then(window.location.reload())
  }

  return (
    <Stack sx={{ ml: 1 }}>
      <NavBar selected="tasks" />
      <ContentBox>
        <Stack>
          {isLoadingTasks ? (
            <CircularProgress />
          ) : tasks.length === 0 ? (
            <Box display="flex" sx={{ m: 2 }} justifyContent="center">
              <Typography>No task in progress</Typography>
            </Box>
          ) : (
            <Stack>
              <Switch label="Auto Refresh" 
              onChange={(event) =>
                setAutoRefresh(event.target.checked)
              }
              />
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
                disableRowSelectionOnClick
                sx={{ m: 1 }}
              />
            </Stack>
          )}
          <Box sx={{ m: 1 }}>
            <ActionButton onClick={apiUpdate} disabled={tasks.length > 0}>
              Fill Knowledge Base
            </ActionButton>
          </Box>
        </Stack>
      </ContentBox>
    </Stack>
  )
}
