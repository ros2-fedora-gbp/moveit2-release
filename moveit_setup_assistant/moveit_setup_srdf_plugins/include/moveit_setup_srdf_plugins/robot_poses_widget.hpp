/*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2012, Willow Garage, Inc.
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/or other materials provided
 *     with the distribution.
 *   * Neither the name of Willow Garage nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 *  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 *  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 *  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 *  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 *  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 *********************************************************************/

/* Author: Dave Coleman */

#pragma once

// Qt
#include <QComboBox>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QScrollArea>
#include <QSlider>
#include <QStackedWidget>
#include <QTableWidget>
#include <QVBoxLayout>

// SA
#include <moveit_setup_framework/qt/setup_step_widget.hpp>
#include <moveit_setup_srdf_plugins/robot_poses.hpp>

namespace moveit_setup
{
namespace srdf_setup
{
class RobotPosesWidget : public SetupStepWidget
{
  Q_OBJECT

public:
  // ******************************************************************************************
  // Public Functions
  // ******************************************************************************************

  void onInit() override;

  /// Received when this widget is chosen from the navigation menu
  void focusGiven() override;

  SetupStep& getSetupStep() override
  {
    return setup_step_;
  }

  // ******************************************************************************************
  // Qt Components
  // ******************************************************************************************
  QTableWidget* data_table_;
  QPushButton* btn_edit_;
  QPushButton* btn_delete_;
  QPushButton* btn_save_;
  QPushButton* btn_cancel_;
  QStackedWidget* stacked_widget_;
  QScrollArea* scroll_area_;
  QVBoxLayout* column2_;
  QLineEdit* pose_name_field_;
  QComboBox* group_name_field_;
  QWidget* joint_list_widget_;
  QVBoxLayout* joint_list_layout_;
  QWidget* pose_list_widget_;
  QWidget* pose_edit_widget_;
  QLabel* collision_warning_;

private Q_SLOTS:

  // ******************************************************************************************
  // Slot Event Functions
  // ******************************************************************************************

  /// Show edit screen
  void showNewScreen();

  /// Edit whatever element is selected
  void editSelected();

  /// Edit the double clicked element
  void editDoubleClicked(int row, int column);

  /// Preview whatever element is selected
  void previewClicked(int row, int column, int previous_row, int previous_column);

  /// Delete currently editing ite
  void deleteSelected();

  /// Save editing changes
  void doneEditing();

  /// Cancel changes
  void cancelEditing();

  /// Run this whenever the group is changed
  void loadJointSliders(const QString& selected);

  /// Show the robot in its default joint positions
  void showDefaultPose();

  /// Play through the poses
  void playPoses();

  /**
   * Call when one of the sliders has its value changed to store its value in kinematic model
   *
   * @param name - name of joint being changed
   * @param value - value of joint
   */
  void updateRobotModel(const std::string& name, double value);

private:
  // ******************************************************************************************
  // Variables
  // ******************************************************************************************

  RobotPoses setup_step_;

  /// Pointer to currently edited group state
  srdf::Model::GroupState* current_edit_pose_;

  // ******************************************************************************************
  // Private Functions
  // ******************************************************************************************

  /**
   * Create the main list view of poses for robot
   *
   * @return the widget
   */
  QWidget* createContentsWidget();

  /**
   * Create the screen for editing poses
   *
   * @return the widget
   */
  QWidget* createEditWidget();

  /**
   * Load the robot poses into the table
   *
   */
  void loadDataTable();

  /**
   * Populate the combo dropdown box with avail group names
   *
   */
  void loadGroupsComboBox();

  /**
   * Edit the pose with the input name
   *
   * @param name name of pose
   */
  void edit(int row);

  /**
   * Show the robot in the current pose
   */
  void showPose(const srdf::Model::GroupState& pose);

  void updateStateAndCollision(const moveit::core::RobotState& robot_state);
};

// ******************************************************************************************
// ******************************************************************************************
// Slider Widget
// ******************************************************************************************
// ******************************************************************************************
class SliderWidget : public QWidget
{
  Q_OBJECT

public:
  // ******************************************************************************************
  // Public Functions
  // ******************************************************************************************

  /**
   * Constructor
   *
   * @param parent - parent QWidget
   * @param joint_model_ - a ptr reference to the joint this widget represents
   */
  SliderWidget(QWidget* parent, const moveit::core::JointModel* joint_model, double init_value);

  /**
   * Deconstructor
   */
  ~SliderWidget() override;

  // ******************************************************************************************
  // Qt Components
  // ******************************************************************************************

  QLabel* joint_label_;
  QSlider* joint_slider_;
  QLineEdit* joint_value_;

private Q_SLOTS:

  // ******************************************************************************************
  // Slot Event Functions
  // ******************************************************************************************

  /// Called when the joint value slider is changed
  void changeJointValue(int value);

  /// Called when the joint value box is changed
  void changeJointSlider();

Q_SIGNALS:

  // ******************************************************************************************
  // Emitted Signal Functions
  // ******************************************************************************************

  /// Indicate joint name and value when slider widget changed
  void jointValueChanged(const std::string& name, double value);

private:
  // ******************************************************************************************
  // Variables
  // ******************************************************************************************

  // Ptr to the joint's data
  const moveit::core::JointModel* joint_model_;

  // Max & min position
  double max_position_;
  double min_position_;

  // ******************************************************************************************
  // Private Functions
  // ******************************************************************************************
};

}  // namespace srdf_setup
}  // namespace moveit_setup

// Declare std::string as metatype so we can use it in a signal
Q_DECLARE_METATYPE(std::string)
