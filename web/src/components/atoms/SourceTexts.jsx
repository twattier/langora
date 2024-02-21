import { useState } from 'react'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'

import { ActionButton } from '../../utils/style/component'
import { DisplayLines } from '../../utils/display'
import { baseURL } from '../../utils/hooks'

export default function SourceTexts(props) {
  const { sourceId, sourceTexts } = props
  const [edit, setEdit] = useState(false)
  const [updatedText, setUpdatedText] = useState({})
  const [updatedTitle, setUpdatedTitle] = useState({})
  const [deleted, setDeleted] = useState({})
  const hasChange =
    Object.keys(updatedText).length +
      Object.keys(updatedTitle).length +
      Object.keys(deleted).length >
    0

  const saveChange = () => {
    const url = `${baseURL}/sources/${sourceId}/sourcetexts`
    const updates = {}
    for (const [key, value] of Object.entries(updatedTitle)) {
      if (deleted[key]) continue
      updates[key] = { id: key, title: value }
    }
    for (const [key, value] of Object.entries(updatedText)) {
      if (deleted[key]) continue
      let upd = updates[key]
      if (!upd) upd = { id: key }
      upd['text'] = value
      updates[key] = upd
    }
    const changes = {
      updated: Object.values(updates),
      deleted: Object.keys(deleted),
    }
    console.log(JSON.stringify(changes))
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(changes),
    })
    // .then(window.location.reload())
  }

  return (
    <Stack>
      <ActionButton
        onClick={() => {
          setEdit(!edit)
        }}
      >
        Edit
      </ActionButton>
      {!hasChange ? null : (
        <ActionButton onClick={saveChange}>Save</ActionButton>
      )}
      {sourceTexts?.map((text) =>
        deleted[text.id] ? null : (
          <Stack key={text.id} sx={{ mt: 1 }}>
            {edit ? (
              <Box display="flex" sx={{ width: '100%' }}>
                <TextField
                  id={`title-${text.id}`}
                  fullWidth
                  defaultValue={updatedTitle[text.id] ?? text.title}
                  onChange={(e) => {
                    let cupd = { ...updatedTitle }
                    cupd[text.id] = e.target.value
                    setUpdatedTitle(cupd)
                  }}
                />
                <ActionButton
                  onClick={() => {
                    let cdel = { ...deleted }
                    cdel[text.id] = true
                    setDeleted(cdel)
                  }}
                >
                  SUPPR
                </ActionButton>
              </Box>
            ) : text.index === 0 ? (
              <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {updatedTitle[text.id] ?? text.title}
              </Typography>
            ) : text.index === 1 ? (
              <Typography
                variant="h6"
                sx={{ fontWeight: 'bold', textDecoration: 'underline' }}
              >
                {updatedTitle[text.id] ?? text.title}
              </Typography>
            ) : (
              <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                {updatedTitle[text.id] ?? text.title}
              </Typography>
            )}

            {edit ? (
              <TextField
                id={`text-${text.id}`}
                fullWidth
                defaultValue={updatedText[text.id] ?? text.text}
                onChange={(e) => {
                  let cupd = { ...updatedText }
                  cupd[text.id] = e.target.value
                  setUpdatedText(cupd)
                }}
                InputProps={{
                  rows: 10,
                  multiline: true,
                  inputComponent: 'textarea',
                }}
              />
            ) : (
              <DisplayLines
                text={updatedText[text.id] ?? text.text}
                variant="body2"
              />
            )}
          </Stack>
        )
      )}
    </Stack>
  )
}
