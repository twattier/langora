import * as React from 'react'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemText from '@mui/material/ListItemText'
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome'
import SearchIcon from '@mui/icons-material/Search'
import Checkbox from '@mui/material/Checkbox'
import CircularProgress from '@mui/material/CircularProgress'

import { ActionButton, ButtonGenAI } from '../../utils/style/component'
import { InputText } from '../../utils/style/component'

import { baseURL } from '../../utils/hooks'

export default function AddTopic() {
  const [suggestedTopics, setSuggestedTopics] = React.useState()
  const [isLoadingSuggestedTopics, setIsLoadingSuggestedTopics] =
    React.useState(false)
  const suggestTopics = () => {
    setIsLoadingSuggestedTopics(true)
    setSuggestedTopics(undefined)
    const url = `${baseURL}/topics/suggest`
    fetch(url, { method: 'GET' })
      .then((response) => response.json())
      .then((data) => setSuggestedTopics(data))
      .then(setIsLoadingSuggestedTopics(false))
  }

  const [selectedTopics, setSelectedTopics] = React.useState([])
  const selectTopic = (topic, checked) => {
    const list = [...selectedTopics]
    if (checked) list.push(topic)
    else {
      const index = list.indexOf(topic)
      list.splice(index, 1)
    }
    setSelectedTopics(list)
  }
  const addSelectedTopics = () => {
    const url = `${baseURL}/topics`
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topics: selectedTopics }),
    }).then((window.location.href = '/knowledges/tasks'))
  }

  return (
    <Stack spacing={1} sx={{ p: 1 }}>
      <Stack direction="row" spacing={1}>
        <InputText sx={{ width: '100%' }} />
        <ActionButton>Add</ActionButton>
      </Stack>
      <ButtonGenAI onClick={suggestTopics}>
        <AutoAwesomeIcon /> Suggest new topics
      </ButtonGenAI>
      {suggestedTopics === undefined ? (
        !isLoadingSuggestedTopics ? null : (
          <CircularProgress />
        )
      ) : (
        <List dense>
          {suggestedTopics?.map((st) => (
            <ListItem>
              <Checkbox
                sx={{ mr: 1 }}
                id={st}
                onChange={(event) =>
                  selectTopic(event.target.id, event.target.checked)
                }
              />
              <SearchIcon sx={{ mr: 1 }} />
              <ListItemText primaryTypographyProps={{ fontSize: '14px' }}>
                {st}
              </ListItemText>
            </ListItem>
          ))}
        </List>
      )}
      {suggestedTopics === undefined ? null : (
        <Stack direction="row" spacing={1} sx={{ ml: 2 }}>
          <ActionButton
            disabled={selectedTopics.length === 0}
            onClick={addSelectedTopics}
          >
            Add
          </ActionButton>
          {selectedTopics.length === 0 ? null : (
            <Typography variant="body1">{`${selectedTopics.length} Topic(s)`}</Typography>
          )}
        </Stack>
      )}
    </Stack>
  )
}
