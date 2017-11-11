import React, { Component } from 'react'
import PropTypes from 'prop-types'

import {ObjToImmArr} from '../helpers'

import ArticleItem from 'components/ArticleItem'
import Pagination from 'components/Pagination'

export default class Articles extends Component{
  static propTypes = {
  }

  state = {
    beginPoint: 0,
    endPoint: 4
  }

  render(){
    const {match} = this.props
    return(
      <div>
        <ul className="articles__list">
          {this.getBody()}
        </ul>
        <Pagination page={match.params.page} amount={this.getPages()} />
      </div>
    )
  }

  getBody = () => {
    const {articles, match} = this.props
    let {beginPoint, endPoint} = this.state
    endPoint = endPoint * match.params.page
    beginPoint = endPoint - 4

    return ObjToImmArr(articles).slice(beginPoint, endPoint).map(item => {
      return <li key={item.id} className="article__item">
        <ArticleItem article={item} />
      </li>
    })
  }

  getPages = () =>{
     const {articles} = this.props
     return Math.ceil(ObjToImmArr(articles).length / 4)
  }
}