import { createContext, useContext, useReducer, useEffect } from 'react'
import { authApi } from '../api/authApi'

const AuthContext = createContext()

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
      return { ...state, user: action.payload, isAuthenticated: true, loading: false }
    case 'LOGOUT':
      return { ...state, user: null, isAuthenticated: false, loading: false }
    case 'SET_LOADING':
      return { ...state, loading: action.payload }
    default:
      return state
  }
}

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isAuthenticated: false,
    loading: true,
  })

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      authApi.getCurrentUser()
        .then(response => {
          dispatch({ type: 'LOGIN_SUCCESS', payload: response.data })
        })
        .catch(() => {
          localStorage.removeItem('access_token')
          dispatch({ type: 'SET_LOADING', payload: false })
        })
    } else {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }, [])

  const login = async (credentials) => {
    const response = await authApi.login(credentials)
    localStorage.setItem('access_token', response.data.access_token)
    
    // Get user data after login
    const userResponse = await authApi.getCurrentUser()
    dispatch({ type: 'LOGIN_SUCCESS', payload: userResponse.data })
    return response.data
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
    localStorage.removeItem('access_token')
    dispatch({ type: 'LOGOUT' })
  }

  const value = {
    ...state,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}