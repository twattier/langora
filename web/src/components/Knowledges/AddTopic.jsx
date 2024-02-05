import * as React from 'react'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemText from '@mui/material/ListItemText'
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome'
import SearchIcon from '@mui/icons-material/Search'
import Checkbox from '@mui/material/Checkbox'

import { ActionButton, ButtonGenAI } from '../../utils/style/component'
import { InputText } from '../../utils/style/component'

import { baseURL } from '../../utils/hooks'

export default function AddTopic() {
  const [suggestedTopics, setSuggestedTopics] = React.useState()
  const suggestTopics = () => {
    const url = `${baseURL}/topics/suggest`
    fetch(url, { method: 'GET' })
      .then((response) => response.json())
      .then((data) => setSuggestedTopics(data))
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

  return (
    <Stack spacing={1} sx={{ p: 1 }}>
      <Stack direction="row" spacing={1}>
        <InputText sx={{ width: '100%' }} />
        <ActionButton>Add</ActionButton>
        <ButtonGenAI onClick={suggestTopics}>
          <AutoAwesomeIcon />
        </ButtonGenAI>
      </Stack>
      {suggestedTopics === undefined ? null : (
        <List>
          {suggestedTopics?.map((st) => (
            <ListItem>
              <Typography variant="body2">
                <Checkbox
                  sx={{ mr: 1 }}
                  id={st}
                  onChange={(event) =>
                    selectTopic(event.target.id, event.target.checked)
                  }
                />
                <SearchIcon sx={{ mr: 1 }} />
                <ListItemText>{st}</ListItemText>
              </Typography>
            </ListItem>
          ))}
        </List>
      )}
      {suggestedTopics === undefined ? null : (
        <Stack direction="row" spacing={1} sx={{ ml: 2 }}>
          <ActionButton disabled={selectedTopics.length === 0}>
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
