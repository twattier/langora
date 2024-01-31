import { createTheme } from '@mui/material/styles'
import { indigo } from '@mui/material/colors'

export const layout = {
  bannerHeight: 100,
}

export const colors = {
  light: '#efefef',
  dark: '#a9a9a9',
}

export const theme = createTheme({
  palette: {
    primary: indigo,
    secondary: {
      main: '#ff383f',
    },
    background: {
      default: '#efefef',
    },
    text: {
      primary: '#000000',
    },
    content: {
      main: '#d0d4e7',
      dark: '#a9a9a9',
      contrastText: '#fff',
    },
  },
  components: {
    MuiGridItem: {
      styleOverrides: {
        root: {
          paddingLeft: 0,
          paddingTop: 0,
        },
      },
    },
  },
})

// theme = createTheme(theme, {
//   components: {
//     MuiGridItem: {
//       styleOverrides: {
//         root: {
//           paddingLeft: 0,
//           paddingTop: 0,
//         },
//       },
//     },
//   },
// })
